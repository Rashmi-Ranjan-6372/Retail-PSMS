from django.db import transaction
from django.core.exceptions import ValidationError as DjangoValidationError
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import (
    PermissionDenied,
    ValidationError,
)

from inventory.models.sales_models import Sales
from inventory.serializers.sales_serializers import SalesSerializer
from inventory.services.sales_service import create_sale

from accounts.permissions import IsAdminOrStaff
from subscriptions.utils import check_subscription_write_access

# =====================================================
# SALES BASE VIEW
# =====================================================


class SalesBaseView:

    def is_platform_admin(self):

        user = self.request.user

        return user.is_superuser or getattr(user, "role", None) == "superadmin"

    def check_write_access(self):

        if self.is_platform_admin():
            return

        retailer = getattr(self.request.user, "retailer", None)

        if not retailer:
            raise PermissionDenied("Retailer account is not associated with this user.")

        check_subscription_write_access(retailer)

    def get_queryset(self):

        user = self.request.user

        queryset = Sales.objects.select_related(
            "retailer",
            "branch",
            "customer",
            "created_by",
        )

        if self.is_platform_admin():
            return queryset

        retailer = getattr(user, "retailer", None)

        if not retailer:
            return queryset.none()

        queryset = queryset.filter(retailer=retailer)

        branch = getattr(user, "branch", None)

        if branch:
            queryset = queryset.filter(branch=branch)

        return queryset

    def get_sale(self, pk):

        return get_object_or_404(
            self.get_queryset(),
            pk=pk,
        )


# =====================================================
# SALES LIST + CREATE
# =====================================================


class SalesListCreateView(
    SalesBaseView,
    APIView,
):

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    # =================================================
    # GET SALES LIST
    # =================================================

    def get(self, request):

        queryset = self.get_queryset().order_by("-id")

        serializer = SalesSerializer(
            queryset,
            many=True,
        )

        return Response(
            {
                "success": True,
                "message": "Sales retrieved successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    # =================================================
    # CREATE SALE
    # =================================================

    @transaction.atomic
    def post(self, request):

        self.check_write_access()

        user = request.user

        retailer = getattr(user, "retailer", None)

        if not retailer:
            raise PermissionDenied(
                "A retailer must be associated with the user to create a sale."
            )

        branch = getattr(user, "branch", None)

        items = request.data.get("items", [])

        if not isinstance(items, list) or not items:
            raise ValidationError({"items": "At least one sale item is required."})

        try:

            sale = create_sale(
                retailer=retailer,
                branch=branch,
                customer=request.data.get("customer"),
                items=items,
                paid_amount=request.data.get(
                    "paid_amount",
                    0,
                ),
                discount=request.data.get(
                    "discount",
                    0,
                ),
                remarks=request.data.get("remarks"),
                created_by=user,
            )

        except (ValueError, DjangoValidationError) as exc:

            raise ValidationError({"error": str(exc)})

        serializer = SalesSerializer(sale)

        return Response(
            {
                "success": True,
                "message": "Sale created successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


# =====================================================
# SALES DETAIL VIEW
# =====================================================


class SalesDetailView(
    SalesBaseView,
    APIView,
):

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    # =================================================
    # RETRIEVE SALE
    # =================================================

    def get(self, request, pk):

        sale = self.get_sale(pk)

        serializer = SalesSerializer(sale)

        return Response(
            {
                "success": True,
                "message": "Sale retrieved successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    # =================================================
    # UPDATE SALE
    # =================================================

    def put(self, request, pk):

        self.check_write_access()

        sale = self.get_sale(pk)

        raise ValidationError(
            "Sales cannot be updated directly after creation. "
            "Use a dedicated sale-editing service that safely "
            "recalculates stock, item totals, discounts, taxes, "
            "and payment balances."
        )

    # =================================================
    # DELETE SALE
    # =================================================

    def delete(self, request, pk):

        self.check_write_access()

        sale = self.get_sale(pk)

        raise ValidationError(
            "Sales cannot be deleted directly. "
            "Use a sale cancellation service to restore stock "
            "and reverse the related financial transactions."
        )

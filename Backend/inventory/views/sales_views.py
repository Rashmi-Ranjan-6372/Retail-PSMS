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
from branches.mixins import BranchFilterMixin

# =====================================================
# SALES BASE VIEW
# =====================================================


class SalesBaseView(BranchFilterMixin, APIView):

    # =================================================
    # BASE QUERYSET
    # =================================================

    def get_base_queryset(self):

        return Sales.objects.select_related(
            "retailer",
            "branch",
            "customer",
            "created_by",
        )

    # =================================================
    # FILTER QUERYSET
    # =================================================

    def get_queryset(self):

        queryset = self.get_base_queryset()

        return self.filter_queryset_by_user(queryset)

    # =================================================
    # CHECK PLATFORM OWNER
    # =================================================

    def check_write_access(self):

        # Platform Owner bypasses subscription restrictions
        if self.is_platform_owner():
            return

        retailer = getattr(
            self.request.user,
            "retailer",
            None,
        )

        if not retailer:

            raise PermissionDenied("Retailer account is not associated with this user.")

        check_subscription_write_access(retailer)

    # =================================================
    # GET SALE OBJECT
    # =================================================

    def get_sale(self, pk):

        return get_object_or_404(
            self.get_queryset(),
            pk=pk,
        )

    # =================================================
    # VALIDATE BRANCH
    # =================================================

    def validate_sale_branch(self, user, branch):

        if not self.is_valid_user_branch(user, branch):

            raise PermissionDenied("You cannot create sales for this branch.")

        return branch

    # =================================================
    # GET CREATE BRANCH
    # =================================================

    def get_create_branch(self, request):

        user = request.user

        # Super Admin can select a branch
        if self.is_super_admin():

            branch_id = request.data.get("branch")

            if not branch_id:

                raise ValidationError(
                    {"branch": "Branch is required to create a sale."}
                )

            from branches.models import Branch

            branch = get_object_or_404(
                Branch,
                pk=branch_id,
                retailer_id=user.retailer_id,
                is_active=True,
                deleted_at__isnull=True,
            )

            return self.validate_sale_branch(
                user,
                branch,
            )

        # Other users use their assigned branch
        branch = getattr(
            user,
            "branch",
            None,
        )

        if not branch:

            raise PermissionDenied(
                "A branch must be associated with the user to create a sale."
            )

        return self.validate_sale_branch(
            user,
            branch,
        )


# =====================================================
# SALES LIST + CREATE
# =====================================================


class SalesListCreateView(SalesBaseView):

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

        retailer = getattr(
            user,
            "retailer",
            None,
        )

        if not retailer:

            raise PermissionDenied(
                "A retailer must be associated with the user to create a sale."
            )

        branch = self.get_create_branch(request)

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

        except (
            ValueError,
            DjangoValidationError,
        ) as exc:

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


class SalesDetailView(SalesBaseView):

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

        self.get_sale(pk)

        self.check_write_access()

        raise ValidationError(
            "Sales cannot be updated directly after creation. "
            "Use a dedicated sale-editing service that safely "
            "recalculates stock, item totals, discounts, taxes, "
            "and payment balances."
        )

    def patch(self, request, pk):

        self.get_sale(pk)

        self.check_write_access()

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

        self.get_sale(pk)

        self.check_write_access()

        raise ValidationError(
            "Sales cannot be deleted directly. "
            "Use a sale cancellation service to restore stock "
            "and reverse the related financial transactions."
        )

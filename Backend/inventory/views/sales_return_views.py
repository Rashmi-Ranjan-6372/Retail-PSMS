from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import (
    PermissionDenied,
    ValidationError,
)

from accounts.permissions import IsAdminOrStaff
from branches.mixins import BranchFilterMixin

from inventory.models.sales_return_models import SalesReturn
from inventory.serializers.sales_return_serializers import (
    SalesReturnSerializer,
)
from inventory.services.sales_return_service import (
    process_sales_return,
)

from subscriptions.utils import check_subscription_write_access

# =====================================================
# SALES RETURN BASE VIEW
# =====================================================


class SalesReturnBaseView(BranchFilterMixin):

    queryset = SalesReturn.objects.select_related(
        "retailer",
        "branch",
        "sales",
        "created_by",
    )

    serializer_class = SalesReturnSerializer

    def check_write_access(self):

        if self.is_platform_owner():
            return

        user = self.request.user

        if not user.retailer_id:
            raise PermissionDenied("Retailer account is not associated with this user.")

        check_subscription_write_access(user.retailer)


# =====================================================
# SALES RETURN LIST + CREATE
# =====================================================


class SalesReturnListCreateView(
    SalesReturnBaseView,
    ListCreateAPIView,
):

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    def perform_create(self, serializer):

        self.check_write_access()

        serializer.save()


# =====================================================
# SALES RETURN DETAIL
# =====================================================


class SalesReturnDetailView(
    SalesReturnBaseView,
    RetrieveUpdateDestroyAPIView,
):

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    lookup_field = "pk"

    @transaction.atomic
    def perform_update(self, serializer):

        self.check_write_access()

        instance = self.get_object()

        if instance.status == "COMPLETED":
            raise ValidationError("A completed sales return cannot be modified.")

        serializer.save(
            retailer=instance.retailer,
            branch=instance.branch,
            sales=instance.sales,
            created_by=instance.created_by,
        )

    def perform_destroy(self, instance):

        self.check_write_access()

        raise ValidationError(
            "Sales returns cannot be deleted directly. "
            "Use a cancellation or reversal workflow."
        )


# =====================================================
# PROCESS SALES RETURN
# =====================================================


class ProcessSalesReturnView(
    SalesReturnBaseView,
    APIView,
):

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    @transaction.atomic
    def post(self, request, pk):

        self.check_write_access()

        sales_return = get_object_or_404(
            self.get_queryset(),
            pk=pk,
        )

        if sales_return.status == "COMPLETED":
            raise ValidationError("Sales return has already been processed.")

        try:
            sales_return = process_sales_return(sales_return.id)

        except ValueError as exc:
            raise ValidationError(str(exc))

        serializer = self.get_serializer(sales_return)

        return Response(
            {
                "success": True,
                "message": "Sales return processed successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

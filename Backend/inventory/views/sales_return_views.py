from django.db import transaction

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError

from inventory.models.sales_return_models import SalesReturn
from inventory.serializers.sales_return_serializers import SalesReturnSerializer
from inventory.services.sales_return_service import process_sales_return

from accounts.permissions import IsAdminOrStaff
from subscriptions.utils import check_subscription_write_access

# =====================================================
# SALES RETURN BASE VIEW
# =====================================================


class SalesReturnBaseView:

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

        queryset = SalesReturn.objects.select_related(
            "retailer",
            "branch",
            "sales",
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


# =====================================================
# SALES RETURN LIST + CREATE
# =====================================================


class SalesReturnListCreateView(
    SalesReturnBaseView,
    ListCreateAPIView,
):

    serializer_class = SalesReturnSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    @transaction.atomic
    def perform_create(self, serializer):

        self.check_write_access()

        user = self.request.user
        retailer = getattr(user, "retailer", None)

        if not retailer:
            raise PermissionDenied(
                "A retailer must be associated with the user to create a sales return."
            )

        sales_return = serializer.save(
            retailer=retailer,
            branch=getattr(user, "branch", None),
            created_by=user,
        )

        process_sales_return(sales_return.id)


# =====================================================
# SALES RETURN DETAIL
# =====================================================


class SalesReturnDetailView(
    SalesReturnBaseView,
    RetrieveUpdateDestroyAPIView,
):

    serializer_class = SalesReturnSerializer

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

        if instance.status == "COMPLETED":
            raise ValidationError(
                "A completed sales return cannot be deleted. "
                "Use a cancellation or reversal workflow."
            )

        raise ValidationError(
            "Sales returns cannot be deleted directly. "
            "Use a cancellation workflow to maintain accurate "
            "inventory and financial records."
        )

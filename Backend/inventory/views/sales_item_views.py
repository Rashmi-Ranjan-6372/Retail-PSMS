from django.db import transaction

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError

from inventory.models.sales_item_models import SalesItem
from inventory.serializers.sales_item_serializers import SalesItemSerializer
from inventory.services.sales_service import update_sales_totals

from accounts.permissions import IsAdminOrStaff
from subscriptions.utils import check_subscription_write_access

# =====================================================
# SALES ITEM BASE VIEW
# =====================================================


class SalesItemBaseView:

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

        queryset = SalesItem.objects.select_related(
            "retailer",
            "branch",
            "sales",
            "product",
            "batch",
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
# SALES ITEM LIST + CREATE
# =====================================================


class SalesItemListCreateView(
    SalesItemBaseView,
    ListCreateAPIView,
):

    serializer_class = SalesItemSerializer

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
                "A retailer must be associated with the user to create a sales item."
            )

        sales_item = serializer.save(
            retailer=retailer,
            branch=getattr(user, "branch", None),
            created_by=user,
        )

        update_sales_totals(sales_item.sales)


# =====================================================
# SALES ITEM DETAIL
# =====================================================


class SalesItemDetailView(
    SalesItemBaseView,
    RetrieveUpdateDestroyAPIView,
):

    serializer_class = SalesItemSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    lookup_field = "pk"

    @transaction.atomic
    def perform_update(self, serializer):

        self.check_write_access()

        instance = self.get_object()

        old_sales = instance.sales

        sales_item = serializer.save(
            retailer=instance.retailer,
            branch=instance.branch,
            sales=instance.sales,
            created_by=instance.created_by,
        )

        update_sales_totals(old_sales)

    def perform_destroy(self, instance):

        self.check_write_access()

        raise ValidationError(
            "Sales items cannot be deleted directly. "
            "Use a sales cancellation or stock-reversal workflow "
            "to restore inventory and recalculate sale totals."
        )

from django.db import transaction

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import (
    PermissionDenied,
    ValidationError,
)

from inventory.models.purchase_return_item_models import PurchaseReturnItem
from inventory.serializers.purchase_return_item_serializers import (
    PurchaseReturnItemSerializer,
)
from inventory.services.purchase_return_item_service import (
    process_purchase_return_item,
)

from accounts.permissions import IsAdminOrStaff
from subscriptions.utils import check_subscription_write_access

# =====================================================
# PURCHASE RETURN ITEM BASE VIEW
# =====================================================


class PurchaseReturnItemBaseView:

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

        queryset = PurchaseReturnItem.objects.select_related(
            "retailer",
            "branch",
            "purchase_return",
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
# PURCHASE RETURN ITEM LIST + CREATE
# =====================================================


class PurchaseReturnItemListCreateView(
    PurchaseReturnItemBaseView,
    ListCreateAPIView,
):

    serializer_class = PurchaseReturnItemSerializer

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
                "A retailer must be associated with the user to create a purchase return item."
            )

        purchase_return_item = serializer.save(
            retailer=retailer,
            branch=getattr(user, "branch", None),
            created_by=user,
        )

        process_purchase_return_item(purchase_return_item)


# =====================================================
# PURCHASE RETURN ITEM DETAIL
# =====================================================


class PurchaseReturnItemDetailView(
    PurchaseReturnItemBaseView,
    RetrieveUpdateDestroyAPIView,
):

    serializer_class = PurchaseReturnItemSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    lookup_field = "pk"

    @transaction.atomic
    def perform_update(self, serializer):

        self.check_write_access()

        instance = self.get_object()

        purchase_return_item = serializer.save(
            retailer=instance.retailer,
            branch=instance.branch,
            purchase_return=instance.purchase_return,
            created_by=instance.created_by,
        )

        process_purchase_return_item(purchase_return_item)

    def perform_destroy(self, instance):

        self.check_write_access()

        raise ValidationError(
            "Processed purchase return items cannot be deleted directly. "
            "Reverse the stock transaction before deleting the item."
        )

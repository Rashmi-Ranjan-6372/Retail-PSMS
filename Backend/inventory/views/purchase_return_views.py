from django.db import transaction

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError

from inventory.models.purchase_return_models import PurchaseReturn
from inventory.serializers.purchase_return_serializers import (
    PurchaseReturnSerializer,
)

from accounts.permissions import IsAdminOrStaff
from subscriptions.utils import check_subscription_write_access

# =====================================================
# PURCHASE RETURN BASE VIEW
# =====================================================


class PurchaseReturnBaseView:

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

        queryset = PurchaseReturn.objects.select_related(
            "retailer",
            "branch",
            "supplier",
            "created_by",
        ).filter(is_deleted=False)

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
# PURCHASE RETURN LIST + CREATE
# =====================================================


class PurchaseReturnListCreateView(
    PurchaseReturnBaseView,
    ListCreateAPIView,
):

    serializer_class = PurchaseReturnSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    @transaction.atomic
    def perform_create(self, serializer):

        self.check_write_access()

        user = self.request.user

        if self.is_platform_admin():
            serializer.save(created_by=user)
            return

        retailer = getattr(user, "retailer", None)

        if not retailer:
            raise PermissionDenied("Retailer account is not associated with this user.")

        serializer.save(
            retailer=retailer,
            branch=getattr(user, "branch", None),
            created_by=user,
        )


# =====================================================
# PURCHASE RETURN DETAIL
# =====================================================


class PurchaseReturnDetailView(
    PurchaseReturnBaseView,
    RetrieveUpdateDestroyAPIView,
):

    serializer_class = PurchaseReturnSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    lookup_field = "pk"

    @transaction.atomic
    def perform_update(self, serializer):

        self.check_write_access()

        instance = self.get_object()

        serializer.save(
            retailer=instance.retailer,
            branch=instance.branch,
            created_by=instance.created_by,
        )

    def perform_destroy(self, instance):

        self.check_write_access()

        raise ValidationError(
            "Purchase returns cannot be deleted directly. "
            "Cancel the purchase return using a stock-reversal "
            "workflow to maintain inventory and financial records."
        )

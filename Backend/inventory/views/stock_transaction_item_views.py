from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError

from inventory.models.stock_transaction_item_models import (
    StockTransactionItem,
)
from inventory.serializers.stock_transaction_item_serializers import (
    StockTransactionItemSerializer,
)

from accounts.permissions import IsAdminOrStaff
from subscriptions.utils import check_subscription_write_access

# =====================================================
# STOCK TRANSACTION ITEM BASE VIEW
# =====================================================


class StockTransactionItemBaseView:

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

        queryset = StockTransactionItem.objects.select_related(
            "retailer",
            "branch",
            "transaction",
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
# STOCK TRANSACTION ITEM LIST + CREATE
# =====================================================


class StockTransactionItemListCreateView(
    StockTransactionItemBaseView,
    ListCreateAPIView,
):

    serializer_class = StockTransactionItemSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    def perform_create(self, serializer):

        self.check_write_access()

        raise ValidationError(
            "Stock transaction items cannot be created directly. "
            "Create them through the Stock Transaction workflow."
        )


# =====================================================
# STOCK TRANSACTION ITEM DETAIL
# =====================================================


class StockTransactionItemDetailView(
    StockTransactionItemBaseView,
    RetrieveUpdateDestroyAPIView,
):

    serializer_class = StockTransactionItemSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    lookup_field = "pk"

    def perform_update(self, serializer):

        self.check_write_access()

        raise ValidationError(
            "Stock transaction items cannot be updated directly. "
            "Create a reversal transaction and a new transaction if correction is required."
        )

    def perform_destroy(self, instance):

        self.check_write_access()

        raise ValidationError(
            "Stock transaction items cannot be deleted. "
            "Use a reversal transaction to maintain inventory history."
        )

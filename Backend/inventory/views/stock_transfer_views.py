from django.db import transaction
from django.db.models import Q

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError

from inventory.models.stock_transfer_models import StockTransfer
from inventory.serializers.stock_transfer_serializers import (
    StockTransferSerializer,
)
from inventory.services.stock_service import process_stock_transfer

from accounts.permissions import IsAdminOrStaff
from subscriptions.utils import check_subscription_write_access

# =====================================================
# STOCK TRANSFER BASE VIEW
# =====================================================


class StockTransferBaseView:

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

        queryset = StockTransfer.objects.select_related(
            "retailer",
            "branch",
            "from_branch",
            "to_branch",
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
            queryset = queryset.filter(
                Q(branch=branch) | Q(from_branch=branch) | Q(to_branch=branch)
            )

        return queryset


# =====================================================
# STOCK TRANSFER LIST + CREATE
# =====================================================


class StockTransferListCreateView(
    StockTransferBaseView,
    ListCreateAPIView,
):

    serializer_class = StockTransferSerializer

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
                "A retailer must be associated with the user to create a stock transfer."
            )

        stock_transfer = serializer.save(
            retailer=retailer,
            branch=getattr(user, "branch", None),
            created_by=user,
        )

        process_stock_transfer(stock_transfer)


# =====================================================
# STOCK TRANSFER DETAIL
# =====================================================


class StockTransferDetailView(
    StockTransferBaseView,
    RetrieveUpdateDestroyAPIView,
):

    serializer_class = StockTransferSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    lookup_field = "pk"

    @transaction.atomic
    def perform_update(self, serializer):

        self.check_write_access()

        raise ValidationError(
            "Stock transfers cannot be updated directly after creation. "
            "Use a transfer cancellation or reversal workflow."
        )

    def perform_destroy(self, instance):

        self.check_write_access()

        raise ValidationError(
            "Stock transfers cannot be deleted directly. "
            "Use a transfer reversal workflow to maintain accurate stock history."
        )

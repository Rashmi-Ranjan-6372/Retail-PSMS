from django.db import transaction

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError

from inventory.models.stock_transaction_models import StockTransaction
from inventory.serializers.stock_transaction_serializers import (
    StockTransactionSerializer,
)

from accounts.permissions import IsAdminOrStaff
from subscriptions.utils import check_subscription_write_access

# =====================================================
# STOCK TRANSACTION BASE VIEW
# =====================================================


class StockTransactionBaseView:

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

        queryset = StockTransaction.objects.select_related(
            "retailer",
            "branch",
            "supplier",
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


# =====================================================
# STOCK TRANSACTION LIST + CREATE
# =====================================================


class StockTransactionListCreateView(
    StockTransactionBaseView,
    ListCreateAPIView,
):

    serializer_class = StockTransactionSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    @transaction.atomic
    def perform_create(self, serializer):

        self.check_write_access()

        user = self.request.user

        retailer = getattr(user, "retailer", None)
        branch = getattr(user, "branch", None)

        if not retailer:
            raise PermissionDenied(
                "A retailer must be associated with the user to create a stock transaction."
            )

        if not branch:
            raise PermissionDenied(
                "A branch must be associated with the user to create a stock transaction."
            )

        serializer.save(
            retailer=retailer,
            branch=branch,
            created_by=user,
        )


# =====================================================
# STOCK TRANSACTION DETAIL
# =====================================================


class StockTransactionDetailView(
    StockTransactionBaseView,
    RetrieveUpdateDestroyAPIView,
):

    serializer_class = StockTransactionSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    lookup_field = "pk"

    @transaction.atomic
    def perform_update(self, serializer):

        self.check_write_access()

        raise ValidationError(
            "Stock transactions cannot be updated directly. "
            "Use a dedicated transaction correction or reversal workflow."
        )

    def perform_destroy(self, instance):

        self.check_write_access()

        raise ValidationError(
            "Stock transactions cannot be deleted directly. "
            "Use a reversal transaction to maintain accurate stock history."
        )

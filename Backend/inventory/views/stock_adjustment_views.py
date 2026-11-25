from django.db import transaction

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError

from inventory.models.stock_adjustment_models import StockAdjustment
from inventory.serializers.stock_adjustment_serializers import (
    StockAdjustmentSerializer,
)
from inventory.services.stock_adjustment_service import (
    process_stock_adjustment,
)

from accounts.permissions import IsAdminOrStaff
from subscriptions.utils import check_subscription_write_access

# =====================================================
# STOCK ADJUSTMENT BASE VIEW
# =====================================================


class StockAdjustmentBaseView:

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

        queryset = StockAdjustment.objects.select_related(
            "retailer",
            "branch",
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
# STOCK ADJUSTMENT LIST + CREATE
# =====================================================


class StockAdjustmentListCreateView(
    StockAdjustmentBaseView,
    ListCreateAPIView,
):

    serializer_class = StockAdjustmentSerializer

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
                "A retailer must be associated with the user to create a stock adjustment."
            )

        adjustment = serializer.save(
            retailer=retailer,
            branch=getattr(user, "branch", None),
            created_by=user,
        )

        process_stock_adjustment(
            adjustment.id,
            request=self.request,
        )


# =====================================================
# STOCK ADJUSTMENT DETAIL
# =====================================================


class StockAdjustmentDetailView(
    StockAdjustmentBaseView,
    RetrieveUpdateDestroyAPIView,
):

    serializer_class = StockAdjustmentSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    lookup_field = "pk"

    @transaction.atomic
    def perform_update(self, serializer):

        self.check_write_access()

        raise ValidationError(
            "Stock adjustments cannot be edited directly after creation. "
            "Create a reversal adjustment and then create a new adjustment."
        )

    def perform_destroy(self, instance):

        self.check_write_access()

        raise ValidationError(
            "Stock adjustments cannot be deleted directly. "
            "Create a reversal adjustment to maintain accurate stock history."
        )

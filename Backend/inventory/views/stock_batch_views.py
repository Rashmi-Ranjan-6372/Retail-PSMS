from django.db import transaction

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError

from inventory.models.stock_batch_models import StockBatch
from inventory.serializers.stock_batch_serializers import StockBatchSerializer

from accounts.permissions import IsSameRetailerAndBranch
from subscriptions.utils import check_subscription_write_access

# =====================================================
# STOCK BATCH BASE VIEW
# =====================================================


class StockBatchBaseView:

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

        queryset = StockBatch.objects.select_related(
            "retailer",
            "branch",
            "product",
            "supplier",
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
# STOCK BATCH LIST + CREATE
# =====================================================


class StockBatchListCreateView(
    StockBatchBaseView,
    ListCreateAPIView,
):

    serializer_class = StockBatchSerializer

    permission_classes = [
        IsAuthenticated,
        IsSameRetailerAndBranch,
    ]

    @transaction.atomic
    def perform_create(self, serializer):

        self.check_write_access()

        user = self.request.user

        retailer = getattr(user, "retailer", None)
        branch = getattr(user, "branch", None)

        if not retailer:
            raise PermissionDenied(
                "A retailer must be associated with the user to create a stock batch."
            )

        if not branch:
            raise PermissionDenied(
                "A branch must be associated with the user to create a stock batch."
            )

        serializer.save(
            retailer=retailer,
            branch=branch,
            created_by=user,
        )


# =====================================================
# STOCK BATCH DETAIL
# =====================================================


class StockBatchDetailView(
    StockBatchBaseView,
    RetrieveUpdateDestroyAPIView,
):

    serializer_class = StockBatchSerializer

    permission_classes = [
        IsAuthenticated,
        IsSameRetailerAndBranch,
    ]

    lookup_field = "pk"

    @transaction.atomic
    def perform_update(self, serializer):

        self.check_write_access()

        protected_fields = [
            "retailer",
            "branch",
            "product",
            "quantity",
            "available_qty",
            "reserved_qty",
        ]

        for field in protected_fields:
            if field in serializer.validated_data:
                raise ValidationError(
                    {
                        field: (
                            f"{field} cannot be changed directly. "
                            "Use the appropriate inventory operation."
                        )
                    }
                )

        serializer.save()

    def perform_destroy(self, instance):

        self.check_write_access()

        raise ValidationError(
            "Stock batches cannot be deleted directly. "
            "Use the appropriate stock adjustment or inventory reversal process."
        )

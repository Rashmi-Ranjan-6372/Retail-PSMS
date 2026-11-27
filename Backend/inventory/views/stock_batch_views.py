
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
from branches.mixins import BranchFilterMixin


# =====================================================
# STOCK BATCH BASE VIEW
# =====================================================

class StockBatchBaseView(BranchFilterMixin):

    queryset = StockBatch.objects.select_related(
        "retailer",
        "branch",
        "product",
        "supplier",
        "created_by",
    )

    def is_platform_owner(self):

        user = self.request.user

        return (
            user.is_superuser
            or getattr(user, "role", None) == "platform_owner"
        )

    def check_write_access(self):

        # Only Platform Owner bypasses subscription validation
        if self.is_platform_owner():
            return

        retailer = getattr(self.request.user, "retailer", None)

        if not retailer:
            raise PermissionDenied(
                "Retailer account is not associated with this user."
            )

        check_subscription_write_access(retailer)


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

        if (
            branch.retailer_id != retailer.id
            or not branch.is_active
            or branch.deleted_at is not None
        ):
            raise PermissionDenied(
                "You cannot create stock batches for this branch."
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

                raise ValidationError({
                    field: (
                        f"{field} cannot be changed directly. "
                        "Use the appropriate inventory operation."
                    )
                })

        serializer.save()

    def perform_destroy(self, instance):

        self.check_write_access()

        raise ValidationError(
            "Stock batches cannot be deleted directly. "
            "Use the appropriate stock adjustment or inventory reversal process."
        )

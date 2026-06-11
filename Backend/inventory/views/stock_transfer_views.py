from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import (IsAuthenticated)
from inventory.models.stock_transfer_models import (StockTransfer)
from inventory.serializers.stock_transfer_serializers import (StockTransferSerializer)
from accounts.permissions import (IsAdminOrStaff)
from inventory.services.stock_service import (process_stock_transfer)
from subscriptions.utils import (check_subscription_write_access, validate_branch_subscription)

# =====================================================
# STOCK TRANSFER LIST + CREATE
# =====================================================

class StockTransferListCreateView(ListCreateAPIView):

    serializer_class = (
        StockTransferSerializer
    )

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    def get_queryset(self):

        user = self.request.user

        queryset = (
            StockTransfer.objects
            .select_related(
                "retailer",
                "branch",
                "from_branch",
                "to_branch",
                "product",
                "batch",
                "created_by",
            )
            .all()
        )

        if (
            user.is_superuser or
            getattr(user, "role", None) == "superadmin"
        ):
            return queryset

        queryset = queryset.filter(
            retailer=user.retailer
        )

        if getattr(user, "branch", None):

            queryset = queryset.filter(
                branch=user.branch
            )

        return queryset

    def perform_create(self, serializer):

        if not self.request.user.is_superuser:
            check_subscription_write_access(
                self.request.user.retailer
            )
            validate_branch_subscription(
                self.request.user.retailer
            )

        stock_transfer = serializer.save(
            retailer=self.request.user.retailer,
            branch=self.request.user.branch,
            created_by=self.request.user,
        )

        process_stock_transfer(stock_transfer)


# =====================================================
# STOCK TRANSFER DETAIL VIEW
# =====================================================

class StockTransferDetailView(RetrieveUpdateDestroyAPIView):

    serializer_class = (
        StockTransferSerializer
    )

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    lookup_field = "pk"

    def get_queryset(self):

        user = self.request.user

        queryset = (
            StockTransfer.objects
            .select_related(
                "retailer",
                "branch",
                "from_branch",
                "to_branch",
                "product",
                "batch",
                "created_by",
            )
            .all()
        )

        if (
            user.is_superuser or
            getattr(user, "role", None) == "superadmin"
        ):
            return queryset

        queryset = queryset.filter(
            retailer=user.retailer
        )

        if getattr(user, "branch", None):

            queryset = queryset.filter(
                branch=user.branch
            )

        return queryset

    def perform_update(self, serializer):

        if not self.request.user.is_superuser:
            check_subscription_write_access(
                self.request.user.retailer
            )
            validate_branch_subscription(
                self.request.user.retailer
            )

        serializer.save()

    def perform_destroy(self, instance):

        if not self.request.user.is_superuser:
            check_subscription_write_access(
                self.request.user.retailer
            )
            validate_branch_subscription(
                self.request.user.retailer
            )

        instance.delete()
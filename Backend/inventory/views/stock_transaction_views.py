from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from inventory.models.stock_transaction_models import (StockTransaction)
from inventory.serializers.stock_transaction_serializers import (StockTransactionSerializer)
from accounts.permissions import (IsAdminOrStaff)
from subscriptions.utils import (check_subscription_write_access, validate_branch_subscription)

# =====================================================
# STOCK TRANSACTION LIST + CREATE
# =====================================================

class StockTransactionListCreateView(ListCreateAPIView):

    serializer_class = StockTransactionSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    def get_queryset(self):

        user = self.request.user

        queryset = (
            StockTransaction.objects
            .select_related(
                "retailer",
                "branch",
                "supplier",
                "customer",
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

        serializer.save(
            retailer=self.request.user.retailer,
            branch=self.request.user.branch,
            created_by=self.request.user,
        )


# =====================================================
# STOCK TRANSACTION DETAIL VIEW
# =====================================================

class StockTransactionDetailView(
    RetrieveUpdateDestroyAPIView
):

    serializer_class = StockTransactionSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    lookup_field = "pk"

    def get_queryset(self):

        user = self.request.user

        queryset = (
            StockTransaction.objects
            .select_related(
                "retailer",
                "branch",
                "supplier",
                "customer",
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
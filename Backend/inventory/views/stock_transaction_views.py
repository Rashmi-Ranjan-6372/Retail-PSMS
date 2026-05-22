from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from inventory.models.stock_transaction_models import (
    StockTransaction
)
from inventory.serializers.stock_transaction_serializers import (
    StockTransactionSerializer
)
from accounts.permissions import (
    IsAdminOrStaff
)


# =====================================================
# STOCK TRANSACTION LIST + CREATE
# =====================================================

class StockTransactionListCreateView(ListCreateAPIView):
    serializer_class = StockTransactionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff,]
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

        # ================= SUPER ADMIN ================= #

        if (
            user.is_superuser or
            getattr(user, "role", None) == "superadmin"
        ):
            return queryset

        # ================= RETAILER FILTER ================= #

        queryset = queryset.filter(
            retailer=user.retailer
        )

        # ================= BRANCH FILTER ================= #

        if getattr(user, "branch", None):

            queryset = queryset.filter(
                branch=user.branch
            )

        return queryset

    def perform_create(self, serializer):

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

        # ================= SUPER ADMIN ================= #

        if (
            user.is_superuser or
            getattr(user, "role", None) == "superadmin"
        ):
            return queryset

        # ================= RETAILER FILTER ================= #

        queryset = queryset.filter(
            retailer=user.retailer
        )

        # ================= BRANCH FILTER ================= #

        if getattr(user, "branch", None):

            queryset = queryset.filter(
                branch=user.branch
            )

        return queryset
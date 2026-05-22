from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)

from rest_framework.permissions import IsAuthenticated

from inventory.models.stock_transaction_item_models import (
    StockTransactionItem
)

from inventory.serializers.stock_transaction_item_serializers import (
    StockTransactionItemSerializer
)

from accounts.permissions import (
    IsAdminOrStaff
)


# =====================================================
# STOCK TRANSACTION ITEM LIST + CREATE
# =====================================================

class StockTransactionItemListCreateView(
    ListCreateAPIView
):

    serializer_class = StockTransactionItemSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    def get_queryset(self):

        user = self.request.user

        queryset = (
            StockTransactionItem.objects
            .select_related(
                "retailer",
                "branch",
                "transaction",
                "product",
                "batch",
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
# STOCK TRANSACTION ITEM DETAIL VIEW
# =====================================================

class StockTransactionItemDetailView(
    RetrieveUpdateDestroyAPIView
):

    serializer_class = (
        StockTransactionItemSerializer
    )

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    lookup_field = "pk"

    def get_queryset(self):

        user = self.request.user

        queryset = (
            StockTransactionItem.objects
            .select_related(
                "retailer",
                "branch",
                "transaction",
                "product",
                "batch",
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
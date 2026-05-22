from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)

from rest_framework.permissions import (
    IsAuthenticated
)

from inventory.models.stock_transfer_models import (
    StockTransfer
)

from inventory.serializers.stock_transfer_serializers import (
    StockTransferSerializer
)

from accounts.permissions import (
    IsAdminOrStaff
)
from inventory.services.stock_service import (
    process_stock_transfer
)

# =====================================================
# STOCK TRANSFER LIST + CREATE
# =====================================================

class StockTransferListCreateView(
    ListCreateAPIView
):

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

        stock_transfer = serializer.save(
            retailer=self.request.user.retailer,
            branch=self.request.user.branch,
            created_by=self.request.user,
        )

        process_stock_transfer(stock_transfer)


# =====================================================
# STOCK TRANSFER DETAIL VIEW
# =====================================================

class StockTransferDetailView(
    RetrieveUpdateDestroyAPIView
):

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
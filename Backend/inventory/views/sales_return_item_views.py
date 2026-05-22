from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)

from rest_framework.permissions import (
    IsAuthenticated
)

from inventory.models.sales_return_item_models import (
    SalesReturnItem
)

from inventory.serializers.sales_return_item_serializers import (
    SalesReturnItemSerializer
)

from accounts.permissions import (
    IsAdminOrStaff
)

from inventory.services.sales_return_item_service import (
    process_sales_return_item
)


# =====================================================
# SALES RETURN ITEM LIST + CREATE
# =====================================================

class SalesReturnItemListCreateView(
    ListCreateAPIView
):

    serializer_class = (
        SalesReturnItemSerializer
    )

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    def get_queryset(self):

        user = self.request.user

        queryset = (
            SalesReturnItem.objects
            .select_related(
                "retailer",
                "branch",
                "sales_return",
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

        sales_return_item = serializer.save(
            retailer=self.request.user.retailer,
            branch=self.request.user.branch,
            created_by=self.request.user,
        )

        # =========================
        # BUSINESS LOGIC
        # =========================

        process_sales_return_item(
            sales_return_item
        )


# =====================================================
# SALES RETURN ITEM DETAIL VIEW
# =====================================================

class SalesReturnItemDetailView(
    RetrieveUpdateDestroyAPIView
):

    serializer_class = (
        SalesReturnItemSerializer
    )

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    lookup_field = "pk"

    def get_queryset(self):

        user = self.request.user

        queryset = (
            SalesReturnItem.objects
            .select_related(
                "retailer",
                "branch",
                "sales_return",
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
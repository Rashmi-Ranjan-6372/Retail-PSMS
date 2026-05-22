from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)

from rest_framework.permissions import (
    IsAuthenticated
)

from inventory.models.purchase_return_item_models import (
    PurchaseReturnItem
)

from inventory.serializers.purchase_return_item_serializers import (
    PurchaseReturnItemSerializer
)

from inventory.services.purchase_return_item_service import (
    process_purchase_return_item
)

from accounts.permissions import (
    IsAdminOrStaff
)


# =====================================================
# PURCHASE RETURN ITEM LIST + CREATE
# =====================================================

class PurchaseReturnItemListCreateView(
    ListCreateAPIView
):

    serializer_class = (
        PurchaseReturnItemSerializer
    )

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    def get_queryset(self):

        user = self.request.user

        queryset = (
            PurchaseReturnItem.objects
            .select_related(
                "retailer",
                "branch",
                "purchase_return",
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

        purchase_return_item = serializer.save(
            retailer=self.request.user.retailer,
            branch=self.request.user.branch,
            created_by=self.request.user,
        )

        # =========================
        # BUSINESS LOGIC
        # =========================

        process_purchase_return_item(
            purchase_return_item
        )


# =====================================================
# PURCHASE RETURN ITEM DETAIL VIEW
# =====================================================

class PurchaseReturnItemDetailView(
    RetrieveUpdateDestroyAPIView
):

    serializer_class = (
        PurchaseReturnItemSerializer
    )

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    lookup_field = "pk"

    def get_queryset(self):

        user = self.request.user

        queryset = (
            PurchaseReturnItem.objects
            .select_related(
                "retailer",
                "branch",
                "purchase_return",
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
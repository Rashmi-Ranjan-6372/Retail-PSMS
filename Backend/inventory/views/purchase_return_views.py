from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)

from rest_framework.permissions import (
    IsAuthenticated
)

from inventory.models.purchase_return_models import (
    PurchaseReturn
)

from inventory.serializers.purchase_return_serializers import (
    PurchaseReturnSerializer
)

from accounts.permissions import (
    IsAdminOrStaff
)


# =====================================================
# PURCHASE RETURN LIST + CREATE
# =====================================================

class PurchaseReturnListCreateView(
    ListCreateAPIView
):

    serializer_class = (
        PurchaseReturnSerializer
    )

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    def get_queryset(self):

        user = self.request.user

        queryset = (
            PurchaseReturn.objects
            .select_related(
                "retailer",
                "branch",
                "supplier",
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
# PURCHASE RETURN DETAIL VIEW
# =====================================================

class PurchaseReturnDetailView(
    RetrieveUpdateDestroyAPIView
):

    serializer_class = (
        PurchaseReturnSerializer
    )

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    lookup_field = "pk"

    def get_queryset(self):

        user = self.request.user

        queryset = (
            PurchaseReturn.objects
            .select_related(
                "retailer",
                "branch",
                "supplier",
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
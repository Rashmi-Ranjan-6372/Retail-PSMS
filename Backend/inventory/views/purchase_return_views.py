from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from inventory.models.purchase_return_models import PurchaseReturn
from inventory.serializers.purchase_return_serializers import PurchaseReturnSerializer

from accounts.permissions import IsAdminOrStaff
from subscriptions.utils import check_subscription_write_access


# =====================================================
# PURCHASE RETURN LIST + CREATE
# =====================================================

class PurchaseReturnListCreateView(ListCreateAPIView):

    serializer_class = PurchaseReturnSerializer

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

        serializer.save(
            retailer=self.request.user.retailer,
            branch=self.request.user.branch,
            created_by=self.request.user,
        )


# =====================================================
# PURCHASE RETURN DETAIL VIEW
# =====================================================

class PurchaseReturnDetailView(RetrieveUpdateDestroyAPIView):

    serializer_class = PurchaseReturnSerializer

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

        serializer.save()

    def perform_destroy(self, instance):

        if not self.request.user.is_superuser:
            check_subscription_write_access(
                self.request.user.retailer
            )

        instance.delete()
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import (IsAuthenticated)
from inventory.models.receipt_models import (Receipt)
from inventory.serializers.receipt_serializers import (ReceiptSerializer)
from inventory.services.receipt_service import (update_receipt_status)
from accounts.permissions import (IsAdminOrStaff)
from subscriptions.utils import (check_subscription_write_access)

# =====================================================
# RECEIPT LIST + CREATE
# =====================================================

class ReceiptListCreateView(ListCreateAPIView):

    serializer_class = (
        ReceiptSerializer
    )

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    def get_queryset(self):

        user = self.request.user

        queryset = (
            Receipt.objects
            .select_related(
                "retailer",
                "branch",
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

        if not self.request.user.is_superuser:
            check_subscription_write_access(
                self.request.user.retailer
            )

        receipt = serializer.save(
            retailer=self.request.user.retailer,
            branch=self.request.user.branch,
            created_by=self.request.user,
        )

        # =========================
        # BUSINESS LOGIC
        # =========================

        update_receipt_status(receipt)


# =====================================================
# RECEIPT DETAIL VIEW
# =====================================================

class ReceiptDetailView(RetrieveUpdateDestroyAPIView):

    serializer_class = (
        ReceiptSerializer
    )

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    lookup_field = "pk"

    def get_queryset(self):

        user = self.request.user

        queryset = (
            Receipt.objects
            .select_related(
                "retailer",
                "branch",
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

        receipt = serializer.save()

        update_receipt_status(receipt)

    def perform_destroy(self, instance):

        if not self.request.user.is_superuser:
            check_subscription_write_access(
                self.request.user.retailer
            )

        instance.delete()
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from inventory.models.payment_models import Payment
from inventory.serializers.payment_serializers import PaymentSerializer
from inventory.services.payment_service import update_payment_status

from accounts.permissions import IsAdminOrStaff
from subscriptions.utils import check_subscription_write_access


# =====================================================
# PAYMENT LIST + CREATE
# =====================================================

class PaymentListCreateView(ListCreateAPIView):

    serializer_class = PaymentSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    def get_queryset(self):

        user = self.request.user

        queryset = (
            Payment.objects
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

        if not self.request.user.is_superuser:
            check_subscription_write_access(
                self.request.user.retailer
            )

        payment = serializer.save(
            retailer=self.request.user.retailer,
            branch=self.request.user.branch,
            created_by=self.request.user,
        )

        update_payment_status(payment)


# =====================================================
# PAYMENT DETAIL VIEW
# =====================================================

class PaymentDetailView(RetrieveUpdateDestroyAPIView):

    serializer_class = PaymentSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    lookup_field = "pk"

    def get_queryset(self):

        user = self.request.user

        queryset = (
            Payment.objects
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

        payment = serializer.save()

        update_payment_status(payment)

    def perform_destroy(self, instance):

        if not self.request.user.is_superuser:
            check_subscription_write_access(
                self.request.user.retailer
            )

        instance.delete()
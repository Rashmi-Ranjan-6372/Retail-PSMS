from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from inventory.models.payment_models import Payment
from inventory.serializers.payment_serializers import PaymentSerializer
from inventory.services.payment_service import update_payment_status

from accounts.permissions import IsAdminOrStaff
from subscriptions.utils import check_subscription_write_access

# =====================================================
# PAYMENT BASE VIEW
# =====================================================


class PaymentBaseView:

    def is_platform_admin(self):

        user = self.request.user

        return user.is_superuser or getattr(user, "role", None) == "superadmin"

    def check_write_access(self):

        if self.is_platform_admin():
            return

        retailer = getattr(self.request.user, "retailer", None)

        if not retailer:
            raise PermissionDenied("Retailer account is not associated with this user.")

        check_subscription_write_access(retailer)

    def get_queryset(self):

        user = self.request.user

        queryset = Payment.objects.select_related(
            "retailer",
            "branch",
            "supplier",
            "created_by",
        )

        if self.is_platform_admin():
            return queryset

        retailer = getattr(user, "retailer", None)

        if not retailer:
            return queryset.none()

        queryset = queryset.filter(retailer=retailer)

        branch = getattr(user, "branch", None)

        if branch:
            queryset = queryset.filter(branch=branch)

        return queryset


# =====================================================
# PAYMENT LIST + CREATE
# =====================================================


class PaymentListCreateView(
    PaymentBaseView,
    ListCreateAPIView,
):

    serializer_class = PaymentSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    def perform_create(self, serializer):

        self.check_write_access()

        user = self.request.user

        retailer = getattr(user, "retailer", None)

        if not retailer:
            raise PermissionDenied("Retailer account is not associated with this user.")

        payment = serializer.save(
            retailer=retailer,
            branch=getattr(user, "branch", None),
            created_by=user,
        )

        update_payment_status(payment)


# =====================================================
# PAYMENT DETAIL
# =====================================================


class PaymentDetailView(
    PaymentBaseView,
    RetrieveUpdateDestroyAPIView,
):

    serializer_class = PaymentSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    lookup_field = "pk"

    def perform_update(self, serializer):

        self.check_write_access()

        instance = self.get_object()

        payment = serializer.save(
            retailer=instance.retailer,
            branch=instance.branch,
            created_by=instance.created_by,
        )

        update_payment_status(payment)

    def perform_destroy(self, instance):

        self.check_write_access()

        instance.delete()

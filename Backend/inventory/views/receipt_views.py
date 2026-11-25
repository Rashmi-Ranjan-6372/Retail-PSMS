from django.db import transaction

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError

from inventory.models.receipt_models import Receipt
from inventory.serializers.receipt_serializers import ReceiptSerializer
from inventory.services.receipt_service import update_receipt_status

from accounts.permissions import IsAdminOrStaff
from subscriptions.utils import check_subscription_write_access

# =====================================================
# RECEIPT BASE VIEW
# =====================================================


class ReceiptBaseView:

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

        queryset = Receipt.objects.select_related(
            "retailer",
            "branch",
            "customer",
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
# RECEIPT LIST + CREATE
# =====================================================


class ReceiptListCreateView(
    ReceiptBaseView,
    ListCreateAPIView,
):

    serializer_class = ReceiptSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    @transaction.atomic
    def perform_create(self, serializer):

        self.check_write_access()

        user = self.request.user

        retailer = getattr(user, "retailer", None)

        if not retailer:
            raise PermissionDenied(
                "A retailer must be associated with the user to create a receipt."
            )

        receipt = serializer.save(
            retailer=retailer,
            branch=getattr(user, "branch", None),
            created_by=user,
        )

        update_receipt_status(receipt)


# =====================================================
# RECEIPT DETAIL
# =====================================================


class ReceiptDetailView(
    ReceiptBaseView,
    RetrieveUpdateDestroyAPIView,
):

    serializer_class = ReceiptSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    lookup_field = "pk"

    @transaction.atomic
    def perform_update(self, serializer):

        self.check_write_access()

        instance = self.get_object()

        receipt = serializer.save(
            retailer=instance.retailer,
            branch=instance.branch,
            created_by=instance.created_by,
        )

        update_receipt_status(receipt)

    def perform_destroy(self, instance):

        self.check_write_access()

        raise ValidationError(
            "Receipts cannot be deleted directly. "
            "Use a receipt cancellation or reversal process "
            "to maintain accurate financial records."
        )

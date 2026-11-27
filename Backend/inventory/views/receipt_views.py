from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from rest_framework.permissions import IsAuthenticated

from rest_framework.exceptions import (
    PermissionDenied,
    ValidationError,
)

from inventory.models.receipt_models import Receipt
from inventory.serializers.receipt_serializers import ReceiptSerializer
from inventory.services.receipt_service import update_receipt_status

from accounts.permissions import IsAdminOrStaff
from subscriptions.utils import check_subscription_write_access
from branches.mixins import BranchFilterMixin
from branches.models import Branch

# =====================================================
# RECEIPT BASE VIEW
# =====================================================


class ReceiptBaseView(BranchFilterMixin):

    # =================================================
    # BASE QUERYSET
    # =================================================

    def get_base_queryset(self):

        return Receipt.objects.select_related(
            "retailer",
            "branch",
            "customer",
            "created_by",
        )

    # =================================================
    # QUERYSET FILTERING
    # =================================================

    def get_queryset(self):

        queryset = self.get_base_queryset()

        return self.filter_queryset_by_user(queryset)

    # =================================================
    # CHECK WRITE ACCESS
    # =================================================

    def check_write_access(self):

        if self.is_platform_owner():
            return

        retailer = getattr(
            self.request.user,
            "retailer",
            None,
        )

        if not retailer:

            raise PermissionDenied("Retailer account is not associated with this user.")

        check_subscription_write_access(retailer)

    # =================================================
    # GET CREATE BRANCH
    # =================================================

    def get_create_branch(self, request):

        user = request.user

        # Super Admin can select a branch
        if self.is_super_admin():

            branch_id = request.data.get("branch")

            if not branch_id:

                raise ValidationError(
                    {"branch": "Branch is required to create a receipt."}
                )

            branch = get_object_or_404(
                Branch,
                pk=branch_id,
                retailer_id=user.retailer_id,
                is_active=True,
                deleted_at__isnull=True,
            )

            return branch

        # Other users use their assigned branch
        branch = getattr(
            user,
            "branch",
            None,
        )

        if not self.is_valid_user_branch(user, branch):

            raise PermissionDenied("You are not assigned to an active branch.")

        return branch


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

    # =================================================
    # CREATE RECEIPT
    # =================================================

    @transaction.atomic
    def perform_create(self, serializer):

        self.check_write_access()

        user = self.request.user

        # =============================================
        # PLATFORM OWNER
        # =============================================

        if self.is_platform_owner():

            retailer = serializer.validated_data.get("retailer")

            if not retailer:

                raise ValidationError({"retailer": "Please select a retailer."})

            branch = serializer.validated_data.get("branch")

            if branch:

                if (
                    branch.retailer_id != retailer.id
                    or not branch.is_active
                    or branch.deleted_at is not None
                ):

                    raise ValidationError(
                        {
                            "branch": "Select an active branch belonging to the selected retailer."
                        }
                    )

        # =============================================
        # RETAILER USERS
        # =============================================

        else:

            retailer = getattr(
                user,
                "retailer",
                None,
            )

            if not retailer:

                raise PermissionDenied(
                    "A retailer must be associated with the user to create a receipt."
                )

            branch = self.get_create_branch(self.request)

        # =============================================
        # SAVE RECEIPT
        # =============================================

        receipt = serializer.save(
            retailer=retailer,
            branch=branch,
            created_by=user,
        )

        # =============================================
        # UPDATE RECEIPT STATUS
        # =============================================

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

    # =================================================
    # UPDATE RECEIPT
    # =================================================

    @transaction.atomic
    def perform_update(self, serializer):

        # Verify object access first
        instance = self.get_object()

        self.check_write_access()

        receipt = serializer.save(
            retailer=instance.retailer,
            branch=instance.branch,
            created_by=instance.created_by,
        )

        update_receipt_status(receipt)

    # =================================================
    # DELETE RECEIPT
    # =================================================

    @transaction.atomic
    def perform_destroy(self, instance):

        self.check_write_access()

        raise ValidationError(
            "Receipts cannot be deleted directly. "
            "Use a receipt cancellation or reversal process "
            "to maintain accurate financial records."
        )

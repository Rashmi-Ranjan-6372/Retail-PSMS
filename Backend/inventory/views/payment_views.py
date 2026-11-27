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

from inventory.models.payment_models import Payment
from inventory.serializers.payment_serializers import PaymentSerializer
from inventory.services.payment_service import update_payment_status

from accounts.permissions import IsAdminOrStaff
from subscriptions.utils import check_subscription_write_access
from branches.mixins import BranchFilterMixin

# =====================================================
# PAYMENT BASE VIEW
# =====================================================


class PaymentBaseView(BranchFilterMixin):

    # =================================================
    # BASE QUERYSET
    # =================================================

    def get_base_queryset(self):

        return Payment.objects.select_related(
            "retailer",
            "branch",
            "supplier",
            "created_by",
        )

    # =================================================
    # QUERYSET FILTERING
    # =================================================

    def get_queryset(self):

        queryset = self.get_base_queryset()

        return self.filter_queryset_by_user(queryset)

    # =================================================
    # WRITE ACCESS
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
    # CREATE BRANCH
    # =================================================

    def get_create_branch(self, request):

        user = request.user

        # Super Admin can select a branch
        if self.is_super_admin():

            branch_id = request.data.get("branch")

            if not branch_id:

                raise ValidationError(
                    {"branch": "Branch is required to create a payment."}
                )

            from branches.models import Branch

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

    # =================================================
    # CREATE PAYMENT
    # =================================================

    @transaction.atomic
    def perform_create(self, serializer):

        self.check_write_access()

        user = self.request.user

        # Platform Owner selects retailer
        if self.is_platform_owner():

            retailer = serializer.validated_data.get("retailer")

            if not retailer:
                raise ValidationError({
                    "retailer": "Please select a retailer."
                })

            branch = serializer.validated_data.get("branch")

            if branch and branch.retailer_id != retailer.id:
                raise ValidationError({
                    "branch": "Branch does not belong to this retailer."
                })

        else:

            retailer = user.retailer
            branch = self.get_create_branch(self.request)

        payment = serializer.save(
            retailer=retailer,
            branch=branch,
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

    # =================================================
    # UPDATE PAYMENT
    # =================================================

    @transaction.atomic
    def perform_update(self, serializer):

        self.check_write_access()

        instance = self.get_object()

        payment = serializer.save(
            retailer=instance.retailer,
            branch=instance.branch,
            created_by=instance.created_by,
        )

        update_payment_status(payment)

    # =================================================
    # DELETE PAYMENT
    # =================================================

    @transaction.atomic
    def perform_destroy(self, instance):

        self.check_write_access()

        instance.delete()

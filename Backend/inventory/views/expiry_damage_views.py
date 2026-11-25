from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from inventory.models.expiry_damage_models import ExpiryDamage
from inventory.serializers.expiry_damage_serializers import ExpiryDamageSerializer

from inventory.services.expiry_service import (
    create_expiry_damage,
    update_expiry_damage,
    delete_expiry_damage,
)

from accounts.permissions import IsAdminOrStaff
from subscriptions.utils import check_subscription_write_access

# =====================================================
# EXPIRY DAMAGE BASE MIXIN
# =====================================================


class ExpiryDamageBaseView:

    def is_platform_admin(self):

        user = self.request.user

        return user.is_superuser or getattr(user, "role", None) == "superadmin"

    def check_write_access(self):

        if self.is_platform_admin():
            return

        retailer = getattr(self.request.user, "retailer", None)

        if not retailer:
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied("Retailer account is not associated with this user.")

        check_subscription_write_access(retailer)

    def get_queryset(self):

        user = self.request.user

        queryset = ExpiryDamage.objects.select_related(
            "retailer",
            "branch",
            "product",
            "batch",
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
# EXPIRY DAMAGE LIST + CREATE
# =====================================================


class ExpiryDamageListCreateView(
    ExpiryDamageBaseView,
    ListCreateAPIView,
):

    serializer_class = ExpiryDamageSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    def perform_create(self, serializer):

        self.check_write_access()

        instance = create_expiry_damage(
            serializer.validated_data,
            self.request.user,
        )

        serializer.instance = instance


# =====================================================
# EXPIRY DAMAGE DETAIL
# =====================================================


class ExpiryDamageDetailView(
    ExpiryDamageBaseView,
    RetrieveUpdateDestroyAPIView,
):

    serializer_class = ExpiryDamageSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    lookup_field = "pk"

    def perform_update(self, serializer):

        self.check_write_access()

        instance = update_expiry_damage(
            self.get_object(),
            serializer.validated_data,
        )

        serializer.instance = instance

    def perform_destroy(self, instance):

        self.check_write_access()

        delete_expiry_damage(instance)

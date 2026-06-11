from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import (IsAuthenticated)
from inventory.models.expiry_damage_models import (ExpiryDamage)
from inventory.serializers.expiry_damage_serializers import (ExpiryDamageSerializer)
from inventory.services.expiry_service import (create_expiry_damage, update_expiry_damage, delete_expiry_damage,)
from accounts.permissions import (IsAdminOrStaff)
from subscriptions.utils import check_subscription_write_access


# =====================================================
# EXPIRY DAMAGE LIST + CREATE
# =====================================================

class ExpiryDamageListCreateView(ListCreateAPIView):

    serializer_class = ExpiryDamageSerializer
    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    def get_queryset(self):

        user = self.request.user

        queryset = (
            ExpiryDamage.objects
            .select_related(
                "retailer",
                "branch",
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

        create_expiry_damage(
            serializer.validated_data,
            self.request.user
        )


# =====================================================
# EXPIRY DAMAGE DETAIL VIEW
# =====================================================

class ExpiryDamageDetailView(RetrieveUpdateDestroyAPIView):

    serializer_class = ExpiryDamageSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    lookup_field = "pk"

    def get_queryset(self):

        user = self.request.user

        queryset = (
            ExpiryDamage.objects
            .select_related(
                "retailer",
                "branch",
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

        update_expiry_damage(
            self.get_object(),
            serializer.validated_data
        )

    def perform_destroy(self, instance):

        if not self.request.user.is_superuser:
            check_subscription_write_access(
                self.request.user.retailer
            )

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from inventory.models.expiry_damage_models import ExpiryDamage
from inventory.serializers.expiry_damage_serializers import (ExpiryDamageSerializer)
from accounts.permissions import (IsSameRetailerAndBranch, IsAdminOrStaff,)

class ExpiryDamageViewSet(ModelViewSet):
    serializer_class = ExpiryDamageSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff, IsSameRetailerAndBranch,]

    def get_queryset(self):

        user = self.request.user

        queryset = ExpiryDamage.objects.select_related(
            "retailer",
            "branch",
            "product",
            "batch",
            "created_by",
        )

        # ================= SUPER ADMIN ================= #

        if (
            getattr(user, "role", None) == "superadmin"
            or user.is_superuser
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

        user = self.request.user

        serializer.save(
            retailer=user.retailer,
            branch=user.branch,
            created_by=user,
        )

    def perform_update(self, serializer):

        serializer.save()

    def perform_destroy(self, instance):

        instance.delete()
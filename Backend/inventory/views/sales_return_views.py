from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import (IsAuthenticated)
from inventory.models.sales_return_models import (SalesReturn)
from inventory.serializers.sales_return_serializers import (SalesReturnSerializer)
from accounts.permissions import (IsAdminOrStaff)
from inventory.services.sales_return_service import (process_sales_return)
from subscriptions.utils import (check_subscription_write_access)

# =====================================================
# SALES RETURN LIST + CREATE
# =====================================================

class SalesReturnListCreateView(ListCreateAPIView):

    serializer_class = SalesReturnSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    def get_queryset(self):

        user = self.request.user

        queryset = (
            SalesReturn.objects
            .select_related(
                "retailer",
                "branch",
                "sales",
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

        sales_return = serializer.save(
            retailer=self.request.user.retailer,
            branch=self.request.user.branch,
            created_by=self.request.user,
        )

        process_sales_return(
            sales_return
        )


# =====================================================
# SALES RETURN DETAIL VIEW
# =====================================================

class SalesReturnDetailView(RetrieveUpdateDestroyAPIView):

    serializer_class = (
        SalesReturnSerializer
    )

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    lookup_field = "pk"

    def get_queryset(self):

        user = self.request.user

        queryset = (
            SalesReturn.objects
            .select_related(
                "retailer",
                "branch",
                "sales",
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
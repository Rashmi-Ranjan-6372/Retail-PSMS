from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated

from inventory.models.stock_batch_models import StockBatch
from inventory.serializers.stock_batch_serializers import (
    StockBatchSerializer
)
from accounts.permissions import (
    IsSameRetailerAndBranch
)


# =========================================
# STOCK BATCH LIST + CREATE
# =========================================

class StockBatchListCreateView(ListCreateAPIView):
    serializer_class = StockBatchSerializer
    permission_classes = [
        IsAuthenticated,
        IsSameRetailerAndBranch
    ]
    def get_queryset(self):
        user = self.request.user
        queryset = StockBatch.objects.all()
        if user.is_superuser or getattr(user, "role", None) == "superadmin":
            return queryset
        queryset = queryset.filter(
            retailer=user.retailer
        )
        if hasattr(user, "branch") and user.branch:
            queryset = queryset.filter(
                branch=user.branch
            )
        return queryset
    def perform_create(self, serializer):

        serializer.save(
            retailer=self.request.user.retailer,
            branch=self.request.user.branch,
            created_by=self.request.user
        )

# =========================================
# STOCK BATCH DETAIL VIEW
# =========================================
class StockBatchDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = StockBatchSerializer
    permission_classes = [
        IsAuthenticated,
        IsSameRetailerAndBranch
    ]
    def get_queryset(self):
        user = self.request.user
        queryset = StockBatch.objects.all()
        if user.is_superuser or getattr(user, "role", None) == "superadmin":
            return queryset
        queryset = queryset.filter(
            retailer=user.retailer
        )
        if hasattr(user, "branch") and user.branch:
            queryset = queryset.filter(
                branch=user.branch
            )

        return queryset
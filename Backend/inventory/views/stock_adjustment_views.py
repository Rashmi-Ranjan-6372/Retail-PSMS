from rest_framework.viewsets import ModelViewSet
from inventory.models.stock_adjustment_models import (
    StockAdjustment
)
from inventory.serializers.stock_adjustment_serializers import (
    StockAdjustmentSerializer
)


class StockAdjustmentViewSet(ModelViewSet):

    queryset = StockAdjustment.objects.all()
    serializer_class = StockAdjustmentSerializer
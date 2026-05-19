from rest_framework.viewsets import ModelViewSet
from inventory.models.stock_batch_models import StockBatch
from inventory.serializers.stock_batch_serializers import (
    StockBatchSerializer
)


class StockBatchViewSet(ModelViewSet):

    queryset = StockBatch.objects.all()
    serializer_class = StockBatchSerializer
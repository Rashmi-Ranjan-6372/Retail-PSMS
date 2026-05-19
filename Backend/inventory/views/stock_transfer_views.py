from rest_framework.viewsets import ModelViewSet
from inventory.models.stock_transfer_models import (
    StockTransfer
)
from inventory.serializers.stock_transfer_serializers import (
    StockTransferSerializer
)


class StockTransferViewSet(ModelViewSet):

    queryset = StockTransfer.objects.all()
    serializer_class = StockTransferSerializer
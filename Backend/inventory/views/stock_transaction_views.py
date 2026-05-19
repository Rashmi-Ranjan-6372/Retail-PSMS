
from rest_framework.viewsets import ModelViewSet
from inventory.models.stock_transaction_models import (
    StockTransaction
)
from inventory.serializers.stock_transaction_serializers import (
    StockTransactionSerializer
)


class StockTransactionViewSet(ModelViewSet):

    queryset = StockTransaction.objects.all()
    serializer_class = StockTransactionSerializer
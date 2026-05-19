from rest_framework import serializers
from inventory.models.stock_transaction_models import (
    StockTransaction
)
from inventory.serializers.stock_transaction_item_serializers import (
    StockTransactionItemSerializer
)


class StockTransactionSerializer(serializers.ModelSerializer):

    items = StockTransactionItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = StockTransaction
        fields = "__all__"
        read_only_fields = [
            "transaction_no",
            "created_at",
            "updated_at",
        ]
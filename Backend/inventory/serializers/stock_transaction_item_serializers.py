from rest_framework import serializers
from inventory.models.stock_transaction_item_models import (
    StockTransactionItem
)


class StockTransactionItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockTransactionItem
        fields = "__all__"
        read_only_fields = [
            "total_amount",
            "created_at",
            "updated_at",
        ]
from rest_framework import serializers
from inventory.models.stock_transfer_models import StockTransfer


class StockTransferSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockTransfer
        fields = "__all__"
        read_only_fields = [
            "transfer_no",
            "total_cost",
            "created_at",
            "updated_at",
        ]
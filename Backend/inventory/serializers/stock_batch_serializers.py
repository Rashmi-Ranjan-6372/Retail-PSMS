from rest_framework import serializers
from inventory.models.stock_batch_models import StockBatch


class StockBatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockBatch
        fields = "__all__"
        read_only_fields = [
            "is_expired",
            "created_at",
            "updated_at",
        ]
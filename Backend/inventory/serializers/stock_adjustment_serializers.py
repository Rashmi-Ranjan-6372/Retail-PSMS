from rest_framework import serializers
from inventory.models.stock_adjustment_models import StockAdjustment


class StockAdjustmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockAdjustment
        fields = "__all__"
        read_only_fields = [
            "total_value",
            "created_at",
            "updated_at",
        ]
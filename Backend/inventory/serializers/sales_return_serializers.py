from rest_framework import serializers
from inventory.models.sales_return_models import SalesReturn
from inventory.serializers.sales_return_item_serializers import (
    SalesReturnItemSerializer
)


class SalesReturnSerializer(serializers.ModelSerializer):

    items = SalesReturnItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = SalesReturn
        fields = "__all__"
        read_only_fields = [
            "return_no",
            "created_at",
            "updated_at",
        ]
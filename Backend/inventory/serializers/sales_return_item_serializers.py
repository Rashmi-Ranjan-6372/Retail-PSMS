from rest_framework import serializers
from inventory.models.sales_return_item_models import SalesReturnItem


class SalesReturnItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = SalesReturnItem
        fields = "__all__"
        read_only_fields = [
            "amount",
            "created_at",
            "updated_at",
        ]
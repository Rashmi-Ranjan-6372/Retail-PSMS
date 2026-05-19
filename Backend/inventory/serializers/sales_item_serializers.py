from rest_framework import serializers
from inventory.models.sales_item_models import SalesItem


class SalesItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = SalesItem
        fields = "__all__"
        read_only_fields = [
            "tax_amount",
            "amount",
            "created_at",
            "updated_at",
        ]
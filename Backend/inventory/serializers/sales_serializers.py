from rest_framework import serializers
from inventory.models.sales_models import Sales
from inventory.serializers.sales_item_serializers import (
    SalesItemSerializer
)


class SalesSerializer(serializers.ModelSerializer):

    items = SalesItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Sales
        fields = "__all__"
        read_only_fields = [
            "invoice_no",
            "net_amount",
            "due_amount",
            "payment_status",
            "created_at",
            "updated_at",
        ]
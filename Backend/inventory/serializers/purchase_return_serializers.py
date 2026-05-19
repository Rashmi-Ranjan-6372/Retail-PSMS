from rest_framework import serializers
from inventory.models.purchase_return_models import PurchaseReturn
from inventory.serializers.purchase_return_item_serializers import (
    PurchaseReturnItemSerializer
)


class PurchaseReturnSerializer(serializers.ModelSerializer):

    items = PurchaseReturnItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = PurchaseReturn
        fields = "__all__"
        read_only_fields = [
            "return_no",
            "created_at",
            "updated_at",
        ]
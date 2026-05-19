from rest_framework import serializers
from inventory.models.purchase_return_item_models import PurchaseReturnItem


class PurchaseReturnItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseReturnItem
        fields = "__all__"
        read_only_fields = [
            "amount",
            "created_at",
            "updated_at",
        ]
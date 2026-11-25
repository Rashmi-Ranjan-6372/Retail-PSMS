
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
            "retailer",
            "return_no",
            "total_amount",
            "adjusted_amount",
            "created_by",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):

        request = self.context.get("request")
        instance = self.instance

        retailer = (
            attrs.get("retailer")
            or getattr(instance, "retailer", None)
        )

        branch = (
            attrs.get("branch")
            if "branch" in attrs
            else getattr(instance, "branch", None)
        )

        supplier = (
            attrs.get("supplier")
            if "supplier" in attrs
            else getattr(instance, "supplier", None)
        )

        if request and request.user.is_authenticated:

            user_retailer = getattr(request.user, "retailer", None)

            if user_retailer:
                retailer = user_retailer

            elif not request.user.is_superuser:
                raise serializers.ValidationError({
                    "retailer": "Retailer account is required."
                })

        if not retailer:
            raise serializers.ValidationError({
                "retailer": "Retailer is required."
            })

        if branch and branch.retailer_id != retailer.id:
            raise serializers.ValidationError({
                "branch": "Branch does not belong to this retailer."
            })

        if supplier and supplier.retailer_id != retailer.id:
            raise serializers.ValidationError({
                "supplier": "Supplier does not belong to this retailer."
            })

        attrs["retailer"] = retailer

        return attrs

    def create(self, validated_data):

        request = self.context.get("request")

        if request and request.user.is_authenticated:
            validated_data["created_by"] = request.user

        return super().create(validated_data)

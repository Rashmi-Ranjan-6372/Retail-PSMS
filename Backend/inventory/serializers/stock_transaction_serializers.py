
from rest_framework import serializers

from inventory.models.stock_transaction_models import StockTransaction
from inventory.serializers.stock_transaction_item_serializers import (
    StockTransactionItemSerializer
)


class StockTransactionSerializer(serializers.ModelSerializer):

    items = StockTransactionItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = StockTransaction
        fields = "__all__"

        read_only_fields = [
            "retailer",
            "transaction_no",
            "total_amount",
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

        branch = attrs.get(
            "branch",
            getattr(instance, "branch", None)
        )

        supplier = attrs.get(
            "supplier",
            getattr(instance, "supplier", None)
        )

        customer = attrs.get(
            "customer",
            getattr(instance, "customer", None)
        )

        if request and request.user.is_authenticated:

            user_retailer = getattr(
                request.user,
                "retailer",
                None
            )

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

        if customer and customer.retailer_id != retailer.id:
            raise serializers.ValidationError({
                "customer": "Customer does not belong to this retailer."
            })

        attrs["retailer"] = retailer

        return attrs

    def create(self, validated_data):

        request = self.context.get("request")

        if request and request.user.is_authenticated:
            validated_data["created_by"] = request.user

        return super().create(validated_data)

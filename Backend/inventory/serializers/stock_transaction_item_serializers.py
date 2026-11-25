
from decimal import Decimal

from rest_framework import serializers

from inventory.models.stock_transaction_item_models import (
    StockTransactionItem
)


class StockTransactionItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockTransactionItem
        fields = "__all__"

        read_only_fields = [
            "retailer",
            "total_amount",
            "available_after",
            "created_by",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):

        request = self.context.get("request")
        instance = self.instance

        transaction = attrs.get(
            "transaction",
            getattr(instance, "transaction", None)
        )

        product = attrs.get(
            "product",
            getattr(instance, "product", None)
        )

        batch = attrs.get(
            "batch",
            getattr(instance, "batch", None)
        )

        branch = attrs.get(
            "branch",
            getattr(instance, "branch", None)
        )

        qty = attrs.get(
            "qty",
            getattr(instance, "qty", 0)
        )

        free_qty = attrs.get(
            "free_qty",
            getattr(instance, "free_qty", 0)
        )

        purchase_price = attrs.get(
            "purchase_price",
            getattr(instance, "purchase_price", 0)
        )

        sale_price = attrs.get(
            "sale_price",
            getattr(instance, "sale_price", 0)
        )

        retailer = transaction.retailer if transaction else None

        if not transaction:
            raise serializers.ValidationError({
                "transaction": "Stock transaction is required."
            })

        if request and request.user.is_authenticated:

            user_retailer = getattr(
                request.user,
                "retailer",
                None
            )

            if user_retailer:

                if retailer and user_retailer.id != retailer.id:
                    raise serializers.ValidationError({
                        "transaction": (
                            "You cannot access another retailer's transaction."
                        )
                    })

            elif not request.user.is_superuser:
                raise serializers.ValidationError({
                    "retailer": "Retailer account is required."
                })

        if not retailer:
            raise serializers.ValidationError({
                "retailer": "Retailer is required."
            })

        if transaction.branch_id != (
            branch.id if branch else None
        ):
            raise serializers.ValidationError({
                "branch": "Branch must match the stock transaction."
            })

        if product and product.retailer_id != retailer.id:
            raise serializers.ValidationError({
                "product": "Product does not belong to this retailer."
            })

        if batch:

            if batch.retailer_id != retailer.id:
                raise serializers.ValidationError({
                    "batch": "Batch does not belong to this retailer."
                })

            if product and batch.product_id != product.id:
                raise serializers.ValidationError({
                    "batch": "Batch does not belong to the selected product."
                })

            if batch.branch_id != (
                branch.id if branch else None
            ):
                raise serializers.ValidationError({
                    "batch": "Batch does not belong to the selected branch."
                })

        if qty <= 0:
            raise serializers.ValidationError({
                "qty": "Quantity must be greater than 0."
            })

        if free_qty < 0:
            raise serializers.ValidationError({
                "free_qty": "Free quantity cannot be negative."
            })

        if purchase_price < 0:
            raise serializers.ValidationError({
                "purchase_price": "Purchase price cannot be negative."
            })

        if sale_price < 0:
            raise serializers.ValidationError({
                "sale_price": "Sale price cannot be negative."
            })

        attrs["retailer"] = retailer

        return attrs

    def create(self, validated_data):

        request = self.context.get("request")

        if request and request.user.is_authenticated:
            validated_data["created_by"] = request.user

        return super().create(validated_data)

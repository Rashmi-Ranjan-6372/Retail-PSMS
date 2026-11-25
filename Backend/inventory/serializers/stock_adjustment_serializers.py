
from rest_framework import serializers

from inventory.models.stock_adjustment_models import StockAdjustment


class StockAdjustmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockAdjustment
        fields = "__all__"

        read_only_fields = [
            "retailer",
            "total_value",
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

        product = attrs.get(
            "product",
            getattr(instance, "product", None)
        )

        batch = attrs.get(
            "batch",
            getattr(instance, "batch", None)
        )

        adjustment_qty = attrs.get(
            "adjustment_qty",
            getattr(instance, "adjustment_qty", 0)
        )

        unit_price = attrs.get(
            "unit_price",
            getattr(instance, "unit_price", 0)
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

            if branch and batch.branch_id != branch.id:
                raise serializers.ValidationError({
                    "batch": "Batch does not belong to the selected branch."
                })

        if adjustment_qty <= 0:
            raise serializers.ValidationError({
                "adjustment_qty": "Adjustment quantity must be greater than 0."
            })

        if unit_price < 0:
            raise serializers.ValidationError({
                "unit_price": "Unit price cannot be negative."
            })

        attrs["retailer"] = retailer

        return attrs

    def create(self, validated_data):

        request = self.context.get("request")

        if request and request.user.is_authenticated:
            validated_data["created_by"] = request.user

        return super().create(validated_data)

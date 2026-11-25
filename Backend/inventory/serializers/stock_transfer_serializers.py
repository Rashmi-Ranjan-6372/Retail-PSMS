
from rest_framework import serializers

from inventory.models.stock_transfer_models import StockTransfer


class StockTransferSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockTransfer
        fields = "__all__"

        read_only_fields = [
            "retailer",
            "transfer_no",
            "total_cost",
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

        from_branch = attrs.get(
            "from_branch",
            getattr(instance, "from_branch", None)
        )

        to_branch = attrs.get(
            "to_branch",
            getattr(instance, "to_branch", None)
        )

        product = attrs.get(
            "product",
            getattr(instance, "product", None)
        )

        batch = attrs.get(
            "batch",
            getattr(instance, "batch", None)
        )

        quantity = attrs.get(
            "quantity",
            getattr(instance, "quantity", 0)
        )

        unit_cost = attrs.get(
            "unit_cost",
            getattr(instance, "unit_cost", 0)
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

        if not from_branch:
            raise serializers.ValidationError({
                "from_branch": "Source branch is required."
            })

        if not to_branch:
            raise serializers.ValidationError({
                "to_branch": "Destination branch is required."
            })

        if from_branch.id == to_branch.id:
            raise serializers.ValidationError({
                "to_branch": (
                    "Source and destination branches cannot be the same."
                )
            })

        if from_branch.retailer_id != retailer.id:
            raise serializers.ValidationError({
                "from_branch": "Source branch does not belong to this retailer."
            })

        if to_branch.retailer_id != retailer.id:
            raise serializers.ValidationError({
                "to_branch": "Destination branch does not belong to this retailer."
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

            if batch.branch_id != from_branch.id:
                raise serializers.ValidationError({
                    "batch": "Selected batch does not belong to the source branch."
                })

        if quantity <= 0:
            raise serializers.ValidationError({
                "quantity": "Transfer quantity must be greater than 0."
            })

        if unit_cost < 0:
            raise serializers.ValidationError({
                "unit_cost": "Unit cost cannot be negative."
            })

        attrs["retailer"] = retailer

        return attrs

    def create(self, validated_data):

        request = self.context.get("request")

        if request and request.user.is_authenticated:
            validated_data["created_by"] = request.user

        return super().create(validated_data)

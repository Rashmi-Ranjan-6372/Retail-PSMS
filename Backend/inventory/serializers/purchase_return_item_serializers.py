
from rest_framework import serializers

from inventory.models.purchase_return_item_models import PurchaseReturnItem


class PurchaseReturnItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseReturnItem
        fields = "__all__"

        read_only_fields = [
            "retailer",
            "amount",
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

        purchase_return = (
            attrs.get("purchase_return")
            or getattr(instance, "purchase_return", None)
        )

        product = (
            attrs.get("product")
            or getattr(instance, "product", None)
        )

        batch = (
            attrs.get("batch")
            or getattr(instance, "batch", None)
        )

        qty = attrs.get(
            "qty",
            getattr(instance, "qty", None)
        )

        free_qty = attrs.get(
            "free_qty",
            getattr(instance, "free_qty", 0)
        )

        unit_price = attrs.get(
            "unit_price",
            getattr(instance, "unit_price", None)
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

        if purchase_return:

            if purchase_return.retailer_id != retailer.id:
                raise serializers.ValidationError({
                    "purchase_return": (
                        "Purchase return does not belong to this retailer."
                    )
                })

            if purchase_return.branch_id != (
                branch.id if branch else None
            ):
                raise serializers.ValidationError({
                    "branch": (
                        "Branch must match the selected purchase return."
                    )
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
                    "batch": "Batch does not belong to this product."
                })

            if branch and batch.branch_id != branch.id:
                raise serializers.ValidationError({
                    "batch": "Batch does not belong to this branch."
                })

        if qty is not None and qty <= 0:
            raise serializers.ValidationError({
                "qty": "Return quantity must be greater than 0."
            })

        if free_qty is not None and free_qty < 0:
            raise serializers.ValidationError({
                "free_qty": "Free quantity cannot be negative."
            })

        if unit_price is not None and unit_price < 0:
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

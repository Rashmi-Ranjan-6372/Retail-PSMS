
from decimal import Decimal

from rest_framework import serializers

from inventory.models.sales_return_item_models import SalesReturnItem


class SalesReturnItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = SalesReturnItem
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

        sales_return = attrs.get(
            "sales_return",
            getattr(instance, "sales_return", None)
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

        unit_price = attrs.get(
            "unit_price",
            getattr(instance, "unit_price", 0)
        )

        discount = attrs.get(
            "discount",
            getattr(instance, "discount", 0)
        )

        retailer = (
            sales_return.retailer
            if sales_return else None
        )

        if request and request.user.is_authenticated:

            user_retailer = getattr(request.user, "retailer", None)

            if user_retailer:
                if retailer and retailer.id != user_retailer.id:
                    raise serializers.ValidationError({
                        "sales_return": (
                            "You cannot access another retailer's sales return."
                        )
                    })
                retailer = user_retailer

            elif not request.user.is_superuser:
                raise serializers.ValidationError({
                    "retailer": "Retailer account is required."
                })

        if not sales_return:
            raise serializers.ValidationError({
                "sales_return": "Sales return is required."
            })

        if not retailer:
            raise serializers.ValidationError({
                "retailer": "Retailer is required."
            })

        if sales_return.retailer_id != retailer.id:
            raise serializers.ValidationError({
                "sales_return": "Sales return does not belong to this retailer."
            })

        if sales_return.branch_id != (
            branch.id if branch else None
        ):
            raise serializers.ValidationError({
                "branch": "Branch must match the selected sales return."
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
                "qty": "Return quantity must be greater than 0."
            })

        if free_qty < 0:
            raise serializers.ValidationError({
                "free_qty": "Free quantity cannot be negative."
            })

        if unit_price < 0:
            raise serializers.ValidationError({
                "unit_price": "Unit price cannot be negative."
            })

        if discount < 0:
            raise serializers.ValidationError({
                "discount": "Discount cannot be negative."
            })

        base_amount = Decimal(str(qty)) * Decimal(str(unit_price))

        if Decimal(str(discount)) > base_amount:
            raise serializers.ValidationError({
                "discount": "Discount cannot exceed the base amount."
            })

        attrs["retailer"] = retailer

        return attrs

    def calculate_amount(self, qty, unit_price, discount):

        base_amount = (
            Decimal(str(qty)) *
            Decimal(str(unit_price))
        )

        amount = base_amount - Decimal(str(discount))

        return amount

    def create(self, validated_data):

        request = self.context.get("request")

        if request and request.user.is_authenticated:
            validated_data["created_by"] = request.user

        qty = validated_data["qty"]
        unit_price = validated_data["unit_price"]
        discount = validated_data.get("discount", 0)

        validated_data["amount"] = self.calculate_amount(
            qty,
            unit_price,
            discount
        )

        return super().create(validated_data)

    def update(self, instance, validated_data):

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.amount = self.calculate_amount(
            instance.qty,
            instance.unit_price,
            instance.discount
        )

        instance.save()

        return instance

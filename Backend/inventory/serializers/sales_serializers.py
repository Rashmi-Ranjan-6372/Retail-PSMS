
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
            "retailer",
            "invoice_no",
            "total_amount",
            "net_amount",
            "due_amount",
            "payment_status",
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

        customer = attrs.get(
            "customer",
            getattr(instance, "customer", None)
        )

        discount = attrs.get(
            "discount",
            getattr(instance, "discount", 0)
        )

        paid_amount = attrs.get(
            "paid_amount",
            getattr(instance, "paid_amount", 0)
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

        if customer and customer.retailer_id != retailer.id:
            raise serializers.ValidationError({
                "customer": "Customer does not belong to this retailer."
            })

        if discount < 0:
            raise serializers.ValidationError({
                "discount": "Discount cannot be negative."
            })

        if paid_amount < 0:
            raise serializers.ValidationError({
                "paid_amount": "Paid amount cannot be negative."
            })

        attrs["retailer"] = retailer

        return attrs

    def create(self, validated_data):

        request = self.context.get("request")

        if request and request.user.is_authenticated:
            validated_data["created_by"] = request.user

        return super().create(validated_data)

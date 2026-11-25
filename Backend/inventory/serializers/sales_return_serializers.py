
from rest_framework import serializers

from inventory.models.sales_return_models import SalesReturn
from inventory.serializers.sales_return_item_serializers import (
    SalesReturnItemSerializer
)


class SalesReturnSerializer(serializers.ModelSerializer):

    items = SalesReturnItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = SalesReturn
        fields = "__all__"

        read_only_fields = [
            "retailer",
            "return_no",
            "total_amount",
            "refund_amount",
            "created_by",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):

        request = self.context.get("request")
        instance = self.instance

        sales = attrs.get(
            "sales",
            getattr(instance, "sales", None)
        )

        branch = attrs.get(
            "branch",
            getattr(instance, "branch", None)
        )

        if not sales:
            raise serializers.ValidationError({
                "sales": "Original sales record is required."
            })

        retailer = sales.retailer

        if request and request.user.is_authenticated:

            user_retailer = getattr(request.user, "retailer", None)

            if user_retailer:
                if user_retailer.id != retailer.id:
                    raise serializers.ValidationError({
                        "sales": (
                            "You cannot access another retailer's sales."
                        )
                    })

            elif not request.user.is_superuser:
                raise serializers.ValidationError({
                    "retailer": "Retailer account is required."
                })

        if sales.branch_id != (
            branch.id if branch else None
        ):
            raise serializers.ValidationError({
                "branch": "Branch must match the original sales record."
            })

        if sales.status == "CANCELLED":
            raise serializers.ValidationError({
                "sales": "Cannot create a return for cancelled sales."
            })

        attrs["retailer"] = retailer

        return attrs

    def create(self, validated_data):

        request = self.context.get("request")

        if request and request.user.is_authenticated:
            validated_data["created_by"] = request.user

        return super().create(validated_data)

from rest_framework import serializers

from inventory.models.sales_return_models import SalesReturn
from inventory.models.sales_models import Sales

from inventory.serializers.sales_return_item_serializers import (
    SalesReturnItemSerializer,
)


class SalesReturnSerializer(serializers.ModelSerializer):

    items = SalesReturnItemSerializer(
        many=True,
        read_only=True,
    )

    retailer_name = serializers.CharField(
        source="retailer.name",
        read_only=True,
    )

    branch_name = serializers.CharField(
        source="branch.name",
        read_only=True,
    )

    sales_no = serializers.CharField(
        source="sales.invoice_no",
        read_only=True,
    )

    created_by_name = serializers.CharField(
        source="created_by.username",
        read_only=True,
    )

    class Meta:
        model = SalesReturn
        fields = "__all__"

        read_only_fields = [
            "retailer",
            "branch",
            "return_no",
            "total_amount",
            "refund_amount",
            "status",
            "created_by",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):

        request = self.context.get("request")
        instance = self.instance

        if instance and instance.status == "COMPLETED":
            raise serializers.ValidationError(
                "A completed sales return cannot be modified."
            )

        sales = attrs.get(
            "sales",
            getattr(instance, "sales", None),
        )

        if not sales:
            raise serializers.ValidationError(
                {"sales": "Original sales record is required."}
            )

        if sales.status == "CANCELLED":
            raise serializers.ValidationError(
                {"sales": "Cannot create a return for cancelled sales."}
            )

        if sales.status not in ["COMPLETED", "PAID", "PARTIAL"]:
            raise serializers.ValidationError(
                {"sales": "Only a completed sale can be returned."}
            )

        if request and request.user.is_authenticated:
            user = request.user

            is_platform_owner = (
                user.is_superuser or getattr(user, "role", None) == "platform_owner"
            )

            if not is_platform_owner:
                if not user.retailer_id:
                    raise serializers.ValidationError(
                        {"sales": "Your account is not associated with a retailer."}
                    )

                if sales.retailer_id != user.retailer_id:
                    raise serializers.ValidationError(
                        {"sales": "You cannot return another retailer's sale."}
                    )

                if not user.is_active:
                    raise serializers.ValidationError(
                        {"sales": "Your account is inactive."}
                    )

                if getattr(user, "role", None) != "superadmin":
                    if not user.branch_id:
                        raise serializers.ValidationError(
                            {"sales": "You are not assigned to a branch."}
                        )

                    if sales.branch_id != user.branch_id:
                        raise serializers.ValidationError(
                            {"sales": "You cannot return a sale from another branch."}
                        )

        if instance and sales.pk != instance.sales_id:
            raise serializers.ValidationError(
                {"sales": "The original sale cannot be changed after creation."}
            )

        return attrs

    def create(self, validated_data):

        request = self.context.get("request")
        sales = validated_data["sales"]

        validated_data["retailer"] = sales.retailer
        validated_data["branch"] = sales.branch

        if request and request.user.is_authenticated:
            validated_data["created_by"] = request.user

        return super().create(validated_data)

    def update(self, instance, validated_data):

        validated_data.pop("sales", None)

        validated_data["retailer"] = instance.retailer
        validated_data["branch"] = instance.branch
        validated_data["created_by"] = instance.created_by

        return super().update(instance, validated_data)

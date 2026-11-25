
from rest_framework import serializers

from inventory.models.payment_models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = "__all__"

        read_only_fields = [
            "retailer",
            "payment_no",
            "due_amount",
            "status",
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

        amount = attrs.get(
            "amount",
            getattr(instance, "amount", None)
        )

        paid_amount = attrs.get(
            "paid_amount",
            getattr(instance, "paid_amount", None)
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

        if amount is not None and amount <= 0:
            raise serializers.ValidationError({
                "amount": "Payment amount must be greater than 0."
            })

        if paid_amount is not None and paid_amount < 0:
            raise serializers.ValidationError({
                "paid_amount": "Paid amount cannot be negative."
            })

        if (
            amount is not None
            and paid_amount is not None
            and paid_amount > amount
        ):
            raise serializers.ValidationError({
                "paid_amount": "Paid amount cannot exceed total amount."
            })

        attrs["retailer"] = retailer

        return attrs

    def create(self, validated_data):

        request = self.context.get("request")

        if request and request.user.is_authenticated:
            validated_data["created_by"] = request.user

        return super().create(validated_data)

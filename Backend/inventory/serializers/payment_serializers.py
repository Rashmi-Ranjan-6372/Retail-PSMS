from rest_framework import serializers

from inventory.models.payment_models import Payment
from accounts.models import Retailer


class PaymentSerializer(serializers.ModelSerializer):

    retailer_name = serializers.CharField(
        source="retailer.name",
        read_only=True,
    )

    branch_name = serializers.CharField(
        source="branch.name",
        read_only=True,
        allow_null=True,
    )

    supplier_name = serializers.CharField(
        source="supplier.name",
        read_only=True,
    )

    created_by_name = serializers.CharField(
        source="created_by.username",
        read_only=True,
        allow_null=True,
    )

    class Meta:

        model = Payment

        fields = "__all__"

        read_only_fields = [
            "payment_no",
            "due_amount",
            "status",
            "created_by",
            "created_at",
            "updated_at",
        ]

    # =====================================================
    # VALIDATION
    # =====================================================

    def validate(self, attrs):

        request = self.context.get("request")
        instance = self.instance

        retailer = attrs.get(
            "retailer",
            getattr(instance, "retailer", None),
        )

        branch = attrs.get(
            "branch",
            getattr(instance, "branch", None),
        )

        supplier = attrs.get(
            "supplier",
            getattr(instance, "supplier", None),
        )

        amount = attrs.get(
            "amount",
            getattr(instance, "amount", None),
        )

        paid_amount = attrs.get(
            "paid_amount",
            getattr(instance, "paid_amount", None),
        )

        # =================================================
        # RETAILER VALIDATION
        # =================================================

        if request and request.user.is_authenticated:

            user = request.user

            if (
                user.is_superuser
                or getattr(
                    user,
                    "role",
                    None,
                )
                == "platform_owner"
            ):

                if not retailer:

                    raise serializers.ValidationError(
                        {"retailer": "Please select a retailer."}
                    )

            else:

                if not user.retailer_id:

                    raise serializers.ValidationError(
                        {"retailer": "Retailer account is required."}
                    )

                retailer = user.retailer

        if not retailer:

            raise serializers.ValidationError({"retailer": "Retailer is required."})

        # =================================================
        # BRANCH VALIDATION
        # =================================================

        if branch:

            if branch.retailer_id != retailer.id:

                raise serializers.ValidationError(
                    {"branch": "Branch does not belong to this retailer."}
                )

            if not branch.is_active or branch.deleted_at is not None:

                raise serializers.ValidationError(
                    {"branch": "Selected branch is inactive or deleted."}
                )

        # =================================================
        # SUPPLIER VALIDATION
        # =================================================

        if supplier:

            if supplier.retailer_id != retailer.id:

                raise serializers.ValidationError(
                    {"supplier": "Supplier does not belong to this retailer."}
                )

        # =================================================
        # AMOUNT VALIDATION
        # =================================================

        if amount is not None and amount <= 0:

            raise serializers.ValidationError(
                {"amount": "Payment amount must be greater than zero."}
            )

        if paid_amount is not None and paid_amount < 0:

            raise serializers.ValidationError(
                {"paid_amount": "Paid amount cannot be negative."}
            )

        if amount is not None and paid_amount is not None and paid_amount > amount:

            raise serializers.ValidationError(
                {"paid_amount": "Paid amount cannot exceed total amount."}
            )

        attrs["retailer"] = retailer

        return attrs

    # =====================================================
    # CREATE
    # =====================================================

    def create(self, validated_data):

        request = self.context.get("request")

        if request and request.user.is_authenticated:

            validated_data["created_by"] = request.user

        return super().create(validated_data)

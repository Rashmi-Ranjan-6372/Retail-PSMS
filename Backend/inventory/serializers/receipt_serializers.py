from rest_framework import serializers

from inventory.models.receipt_models import Receipt


class ReceiptSerializer(serializers.ModelSerializer):

    retailer_name = serializers.CharField(
        source="retailer.name",
        read_only=True,
    )

    branch_name = serializers.CharField(
        source="branch.name",
        read_only=True,
        allow_null=True,
    )

    customer_name = serializers.CharField(
        source="customer.name",
        read_only=True,
    )

    created_by_name = serializers.CharField(
        source="created_by.username",
        read_only=True,
        allow_null=True,
    )

    class Meta:

        model = Receipt

        fields = "__all__"

        read_only_fields = [
            "receipt_no",
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

        customer = attrs.get(
            "customer",
            getattr(instance, "customer", None),
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

            is_platform_owner = (
                user.is_superuser or getattr(user, "role", None) == "platform_owner"
            )

            if instance:

                # Existing receipt cannot change retailer
                if "retailer" in attrs and attrs["retailer"].id != instance.retailer_id:

                    raise serializers.ValidationError(
                        {"retailer": "Receipt retailer cannot be changed."}
                    )

                retailer = instance.retailer

            elif is_platform_owner:

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

        if instance and "branch" in attrs:

            if (attrs["branch"].id if attrs["branch"] else None) != instance.branch_id:

                raise serializers.ValidationError(
                    {"branch": "Receipt branch cannot be changed."}
                )

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
        # CUSTOMER VALIDATION
        # =================================================

        if customer and customer.retailer_id != retailer.id:

            raise serializers.ValidationError(
                {"customer": "Customer does not belong to this retailer."}
            )

        # =================================================
        # AMOUNT VALIDATION
        # =================================================

        if amount is not None and amount <= 0:

            raise serializers.ValidationError(
                {"amount": "Receipt amount must be greater than zero."}
            )

        if paid_amount is not None and paid_amount < 0:

            raise serializers.ValidationError(
                {"paid_amount": "Paid amount cannot be negative."}
            )

        if amount is not None and paid_amount is not None and paid_amount > amount:

            raise serializers.ValidationError(
                {"paid_amount": "Paid amount cannot exceed receipt amount."}
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

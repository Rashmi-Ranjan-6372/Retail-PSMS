
from rest_framework import serializers

from masters.models.sales_offer_models import SalesOffer


class SalesOfferSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(
        source="product.name",
        read_only=True,
        allow_null=True
    )
    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
        allow_null=True
    )
    manufacturer_name = serializers.CharField(
        source="manufacturer.name",
        read_only=True,
        allow_null=True
    )
    retailer_name = serializers.CharField(
        source="retailer.name",
        read_only=True
    )
    branch_name = serializers.CharField(
        source="branch.name",
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = SalesOffer

        fields = [
            "id",
            "retailer",
            "retailer_name",
            "branch",
            "branch_name",
            "name",
            "offer_type",
            "discount_type",
            "product",
            "product_name",
            "category",
            "category_name",
            "manufacturer",
            "manufacturer_name",
            "discount_percentage",
            "flat_discount_amount",
            "buy_quantity",
            "free_quantity",
            "minimum_quantity",
            "minimum_bill_amount",
            "expiry_before_days",
            "member_type",
            "start_date",
            "end_date",
            "is_active",
            "deleted_at",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "retailer",
            "branch",
            "retailer_name",
            "branch_name",
            "is_active",
            "deleted_at",
            "created_at",
            "updated_at",
        ]

    # =====================================================
    # NAME VALIDATION
    # =====================================================

    def validate_name(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Offer name is required."
            )

        return value

    # =====================================================
    # MAIN VALIDATION
    # =====================================================

    def validate(self, attrs):

        request = self.context.get("request")

        if not request:
            raise serializers.ValidationError(
                "Request context is required."
            )

        user = request.user

        # =================================================
        # GET RETAILER
        # =================================================

        if self.instance:

            retailer = self.instance.retailer

        elif user.is_superuser:

            retailer_id = request.data.get("retailer")

            if not retailer_id:
                raise serializers.ValidationError({
                    "retailer": "Retailer is required."
                })

            from accounts.models import Retailer

            try:
                retailer = Retailer.objects.get(
                    id=retailer_id
                )
            except (Retailer.DoesNotExist, ValueError, TypeError):
                raise serializers.ValidationError({
                    "retailer": "Invalid retailer."
                })

        else:

            retailer = getattr(user, "retailer", None)

            if not retailer:
                raise serializers.ValidationError(
                    "Retailer account is not assigned."
                )

        # =================================================
        # GET EXISTING OR SUBMITTED VALUES
        # =================================================

        product = attrs.get(
            "product",
            getattr(self.instance, "product", None)
        )

        category = attrs.get(
            "category",
            getattr(self.instance, "category", None)
        )

        manufacturer = attrs.get(
            "manufacturer",
            getattr(self.instance, "manufacturer", None)
        )

        start_date = attrs.get(
            "start_date",
            getattr(self.instance, "start_date", None)
        )

        end_date = attrs.get(
            "end_date",
            getattr(self.instance, "end_date", None)
        )

        offer_type = attrs.get(
            "offer_type",
            getattr(self.instance, "offer_type", None)
        )

        discount_type = attrs.get(
            "discount_type",
            getattr(self.instance, "discount_type", "PERCENTAGE")
        )

        discount_percentage = attrs.get(
            "discount_percentage",
            getattr(self.instance, "discount_percentage", None)
        )

        flat_discount_amount = attrs.get(
            "flat_discount_amount",
            getattr(self.instance, "flat_discount_amount", None)
        )

        buy_quantity = attrs.get(
            "buy_quantity",
            getattr(self.instance, "buy_quantity", None)
        )

        free_quantity = attrs.get(
            "free_quantity",
            getattr(self.instance, "free_quantity", None)
        )

        minimum_quantity = attrs.get(
            "minimum_quantity",
            getattr(self.instance, "minimum_quantity", None)
        )

        minimum_bill_amount = attrs.get(
            "minimum_bill_amount",
            getattr(self.instance, "minimum_bill_amount", None)
        )

        expiry_before_days = attrs.get(
            "expiry_before_days",
            getattr(self.instance, "expiry_before_days", None)
        )

        member_type = attrs.get(
            "member_type",
            getattr(self.instance, "member_type", None)
        )

        # =================================================
        # PRODUCT VALIDATION
        # =================================================

        if product:

            if product.retailer_id != retailer.id:
                raise serializers.ValidationError({
                    "product": "Product does not belong to this retailer."
                })

            if not product.is_active:
                raise serializers.ValidationError({
                    "product": "Inactive product cannot be used."
                })

        # =================================================
        # CATEGORY VALIDATION
        # =================================================

        if category:

            if category.retailer_id != retailer.id:
                raise serializers.ValidationError({
                    "category": "Category does not belong to this retailer."
                })

            if not category.is_active:
                raise serializers.ValidationError({
                    "category": "Inactive category cannot be used."
                })

        # =================================================
        # MANUFACTURER VALIDATION
        # =================================================

        if manufacturer:

            if manufacturer.retailer_id != retailer.id:
                raise serializers.ValidationError({
                    "manufacturer": "Manufacturer does not belong to this retailer."
                })

            if not manufacturer.is_active:
                raise serializers.ValidationError({
                    "manufacturer": "Inactive manufacturer cannot be used."
                })

        # =================================================
        # DATE VALIDATION
        # =================================================

        if start_date and end_date:

            if start_date > end_date:
                raise serializers.ValidationError({
                    "end_date": "End date cannot be earlier than start date."
                })

        # =================================================
        # DISCOUNT TYPE VALIDATION
        # =================================================

        if discount_type == "PERCENTAGE":

            if discount_percentage is None:
                raise serializers.ValidationError({
                    "discount_percentage": "Discount percentage is required."
                })

            if not 0 < discount_percentage <= 100:
                raise serializers.ValidationError({
                    "discount_percentage": "Discount percentage must be greater than 0 and cannot exceed 100."
                })

        elif discount_type == "FLAT":

            if flat_discount_amount is None:
                raise serializers.ValidationError({
                    "flat_discount_amount": "Flat discount amount is required."
                })

            if flat_discount_amount <= 0:
                raise serializers.ValidationError({
                    "flat_discount_amount": "Flat discount amount must be greater than 0."
                })

        else:

            raise serializers.ValidationError({
                "discount_type": "Invalid discount type."
            })

        # =================================================
        # OFFER TYPE VALIDATION
        # =================================================

        if offer_type == "PRODUCT_DISCOUNT":

            if not product:
                raise serializers.ValidationError({
                    "product": "Product is required for product discount."
                })

        elif offer_type == "CATEGORY_DISCOUNT":

            if not category:
                raise serializers.ValidationError({
                    "category": "Category is required for category discount."
                })

        elif offer_type == "MANUFACTURER_DISCOUNT":

            if not manufacturer:
                raise serializers.ValidationError({
                    "manufacturer": "Manufacturer is required for manufacturer discount."
                })

        elif offer_type == "BUY_X_GET_Y":

            if not buy_quantity or buy_quantity < 1:
                raise serializers.ValidationError({
                    "buy_quantity": "Buy quantity must be at least 1."
                })

            if not free_quantity or free_quantity < 1:
                raise serializers.ValidationError({
                    "free_quantity": "Free quantity must be at least 1."
                })

        elif offer_type == "QUANTITY_DISCOUNT":

            if not minimum_quantity or minimum_quantity < 1:
                raise serializers.ValidationError({
                    "minimum_quantity": "Minimum quantity must be at least 1."
                })

        elif offer_type == "BILL_AMOUNT_DISCOUNT":

            if minimum_bill_amount is None or minimum_bill_amount <= 0:
                raise serializers.ValidationError({
                    "minimum_bill_amount": "Minimum bill amount must be greater than 0."
                })

        elif offer_type == "EXPIRY_CLEARANCE":

            if expiry_before_days is None or expiry_before_days < 1:
                raise serializers.ValidationError({
                    "expiry_before_days": "Expiry days must be at least 1."
                })

        elif offer_type == "MEMBER_DISCOUNT":

            if not member_type or not member_type.strip():
                raise serializers.ValidationError({
                    "member_type": "Member type is required."
                })

        return attrs

    # =====================================================
    # CREATE
    # =====================================================

    def create(self, validated_data):

        return super().create(validated_data)

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, instance, validated_data):

        # Retailer and branch are controlled by the view.
        validated_data.pop("retailer", None)
        validated_data.pop("branch", None)

        return super().update(instance, validated_data)

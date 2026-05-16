from rest_framework import serializers

from masters.models.sales_offer_models import SalesOffer


class SalesOfferSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )

    manufacturer_name = serializers.CharField(
        source="manufacturer.name",
        read_only=True
    )

    retailer_name = serializers.CharField(
        source="retailer.name",
        read_only=True
    )

    branch_name = serializers.CharField(
        source="branch.name",
        read_only=True
    )

    class Meta:
        model = SalesOffer

        fields = [
            "id",

            # ================= RETAILER =================
            "retailer",
            "retailer_name",

            # ================= BRANCH =================
            "branch",
            "branch_name",

            # ================= BASIC =================
            "name",
            "offer_type",
            "discount_type",

            # ================= TARGET =================
            "product",
            "product_name",

            "category",
            "category_name",

            "manufacturer",
            "manufacturer_name",

            # ================= DISCOUNT =================
            "discount_percentage",
            "flat_discount_amount",

            # ================= BUY X GET Y =================
            "buy_quantity",
            "free_quantity",

            # ================= CONDITIONS =================
            "minimum_quantity",
            "minimum_bill_amount",

            # ================= SPECIAL =================
            "expiry_before_days",
            "member_type",

            # ================= DATES =================
            "start_date",
            "end_date",

            # ================= STATUS =================
            "is_active",

            # ================= TIMESTAMPS =================
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "retailer",
            "branch",
            "retailer_name",
            "branch_name",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):

        request = self.context["request"]
        user = request.user

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

        # ================= RETAILER CHECK =================

        if (
            product and
            product.retailer != user.retailer
        ):
            raise serializers.ValidationError({
                "product": "Invalid retailer product"
            })

        if (
            category and
            category.retailer != user.retailer
        ):
            raise serializers.ValidationError({
                "category": "Invalid retailer category"
            })

        if (
            manufacturer and
            manufacturer.retailer != user.retailer
        ):
            raise serializers.ValidationError({
                "manufacturer": "Invalid retailer manufacturer"
            })

        # ================= DATE CHECK =================

        if start_date and end_date:

            if start_date > end_date:
                raise serializers.ValidationError({
                    "end_date":
                    "End date must be greater than start date"
                })

        # ================= OFFER VALIDATION =================

        if offer_type == "PRODUCT_DISCOUNT" and not product:
            raise serializers.ValidationError({
                "product":
                "Product is required for product discount"
            })

        if offer_type == "CATEGORY_DISCOUNT" and not category:
            raise serializers.ValidationError({
                "category":
                "Category is required for category discount"
            })

        if (
            offer_type == "MANUFACTURER_DISCOUNT" and
            not manufacturer
        ):
            raise serializers.ValidationError({
                "manufacturer":
                "Manufacturer is required"
            })

        if offer_type == "BUY_X_GET_Y":

            if not attrs.get("buy_quantity"):
                raise serializers.ValidationError({
                    "buy_quantity":
                    "Buy quantity is required"
                })

            if not attrs.get("free_quantity"):
                raise serializers.ValidationError({
                    "free_quantity":
                    "Free quantity is required"
                })

        return attrs

    def create(self, validated_data):

        request = self.context["request"]
        user = request.user

        validated_data["retailer"] = user.retailer
        validated_data["branch"] = user.branch

        return super().create(validated_data)

    def update(self, instance, validated_data):

        validated_data.pop("retailer", None)
        validated_data.pop("branch", None)

        return super().update(instance, validated_data)
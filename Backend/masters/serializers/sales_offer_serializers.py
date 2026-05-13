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

    class Meta:
        model = SalesOffer

        fields = [
            "id",
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

            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]
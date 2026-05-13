from rest_framework import serializers

from masters.models.products_models import Product


class ProductSerializer(serializers.ModelSerializer):

    category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )

    manufacturer_name = serializers.CharField(
        source="manufacturer.name",
        read_only=True
    )

    class Meta:
        model = Product

        fields = [
            "id",
            "name",
            "category",
            "category_name",
            "manufacturer",
            "manufacturer_name",
            "strength",
            "units_per_strip",
            "loose_sale_allowed",
            "prescription_required",
            "rack_no",
            "minimum_stock",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]
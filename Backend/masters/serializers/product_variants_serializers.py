from rest_framework import serializers
from masters.models.product_variants_models import ProductVariant
from masters.models.products_models import Product


class ProductVariantSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "product",
            "product_name",
            "variant_name",
            "units_per_pack",
            "loose_sale_allowed",
            "barcode",
            "sku",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_product(self, product):
        request = self.context.get("request")

        if not request:
            return product

        user = request.user

        is_platform_admin = (
            user.is_superuser or getattr(user, "role", None) == "superadmin"
        )

        if is_platform_admin:
            return product

        retailer = getattr(user, "retailer", None)

        if not retailer:
            raise serializers.ValidationError("Retailer account not found.")

        if product.retailer_id != retailer.id:
            raise serializers.ValidationError(
                "You cannot use another retailer's product."
            )

        return product

    def validate_variant_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Variant name is required.")

        return value

    def validate_units_per_pack(self, value):
        if value < 1:
            raise serializers.ValidationError("Units per pack must be at least 1.")

        return value

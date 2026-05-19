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
            "retailer",
            "branch",
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
            "retailer",
            "branch",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):

        request = self.context["request"]
        user = request.user

        category = attrs.get(
            "category",
            getattr(self.instance, "category", None)
        )

        manufacturer = attrs.get(
            "manufacturer",
            getattr(self.instance, "manufacturer", None)
        )

        name = attrs.get(
            "name",
            getattr(self.instance, "name", None)
        )

        strength = attrs.get(
            "strength",
            getattr(self.instance, "strength", None)
        )

        # ================= CATEGORY RETAILER CHECK ================= #

        if category and category.retailer != user.retailer:
            raise serializers.ValidationError({
                "category": "Invalid category for this retailer"
            })

        # ================= MANUFACTURER RETAILER CHECK ================= #

        if manufacturer and manufacturer.retailer != user.retailer:
            raise serializers.ValidationError({
                "manufacturer": "Invalid manufacturer for this retailer"
            })

        # ================= UNIQUE PRODUCT CHECK ================= #

        queryset = Product.objects.filter(
            retailer=user.retailer,
            name__iexact=name,
            manufacturer=manufacturer,
            strength=strength
        )

        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)

        if queryset.exists():
            raise serializers.ValidationError({
                "name": (
                    "Product with same name, manufacturer "
                    "and strength already exists"
                )
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
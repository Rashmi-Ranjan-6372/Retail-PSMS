from rest_framework import serializers

from masters.models.products_models import Product


class ProductSerializer(serializers.ModelSerializer):

    category_name = serializers.CharField(source="category.name", read_only=True)
    manufacturer_name = serializers.CharField(
        source="manufacturer.name", read_only=True
    )

    class Meta:
        model = Product

        fields = [
            "id",
            "retailer",
            "name",
            "category",
            "category_name",
            "manufacturer",
            "manufacturer_name",
            "strength",
            "prescription_required",
            "is_active",
            "deleted_at",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "retailer",
            "is_active",
            "deleted_at",
            "created_at",
            "updated_at",
        ]

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Product name is required.")

        return value

    def validate_strength(self, value):
        return (value or "").strip()

    def validate(self, attrs):

        request = self.context.get("request")

        if not request:
            raise serializers.ValidationError("Request context is required.")

        user = request.user
        retailer = getattr(user, "retailer", None)

        if not user.is_superuser and not retailer:
            raise serializers.ValidationError("Retailer account is not assigned.")

        category = attrs.get("category", getattr(self.instance, "category", None))
        manufacturer = attrs.get(
            "manufacturer", getattr(self.instance, "manufacturer", None)
        )
        name = attrs.get("name", getattr(self.instance, "name", None))
        strength = attrs.get("strength", getattr(self.instance, "strength", "")) or ""

        if category:

            if not user.is_superuser and category.retailer_id != retailer.id:
                raise serializers.ValidationError(
                    {"category": "Category does not belong to this retailer."}
                )

            if not category.is_active:
                raise serializers.ValidationError(
                    {"category": "Cannot use an inactive category."}
                )

        if manufacturer:

            if not user.is_superuser and manufacturer.retailer_id != retailer.id:
                raise serializers.ValidationError(
                    {"manufacturer": "Manufacturer does not belong to this retailer."}
                )

            if not manufacturer.is_active:
                raise serializers.ValidationError(
                    {"manufacturer": "Cannot use an inactive manufacturer."}
                )

        if name and manufacturer:

            product_retailer = (
                retailer if retailer else getattr(self.instance, "retailer", None)
            )

            if not product_retailer:
                raise serializers.ValidationError({"retailer": "Retailer is required."})

            queryset = Product.objects.filter(
                retailer=product_retailer,
                name__iexact=name,
                manufacturer=manufacturer,
                strength__iexact=strength,
            )

            if self.instance:
                queryset = queryset.exclude(id=self.instance.id)

            if queryset.exists():
                raise serializers.ValidationError(
                    {
                        "name": "Product with the same name, manufacturer and strength already exists."
                    }
                )

        return attrs

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user

        if not user.is_superuser and not user.retailer_id:
            raise serializers.ValidationError("Retailer account is not assigned.")

        if not user.is_superuser:
            validated_data["retailer"] = user.retailer

        return super().create(validated_data)

    def update(self, instance, validated_data):

        validated_data.pop("retailer", None)

        return super().update(instance, validated_data)

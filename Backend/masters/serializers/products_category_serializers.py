from rest_framework import serializers
from masters.models.products_category_models import Category


class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"

        read_only_fields = (
            "id",
            "retailer",
            "branch",
            "created_at",
            "updated_at",
        )

    def validate_name(self, value):

        value = value.strip().title()

        user = self.context["request"].user

        queryset = Category.objects.filter(
            retailer=user.retailer,
            name__iexact=value
        )

        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)

        if queryset.exists():
            raise serializers.ValidationError(
                "Category name already exists"
            )

        return value

    def validate_code(self, value):

        if value:
            value = value.strip().upper()

            user = self.context["request"].user

            queryset = Category.objects.filter(
                retailer=user.retailer,
                code__iexact=value
            )

            if self.instance:
                queryset = queryset.exclude(id=self.instance.id)

            if queryset.exists():
                raise serializers.ValidationError(
                    "Category code already exists"
                )

        return value

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
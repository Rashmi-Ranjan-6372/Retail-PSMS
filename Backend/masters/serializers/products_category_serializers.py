from rest_framework import serializers

from masters.models.products_category_models import Category
from branches.models import Branch


class ProductCategorySerializer(serializers.ModelSerializer):

    retailer_name = serializers.CharField(source="retailer.name", read_only=True)

    branch_name = serializers.CharField(
        source="branch.name", read_only=True, allow_null=True
    )

    class Meta:
        model = Category

        fields = [
            "id",
            "retailer",
            "retailer_name",
            "branch",
            "branch_name",
            "name",
            "code",
            "description",
            "is_active",
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

    def validate_name(self, value):

        value = value.strip().title()

        request = self.context.get("request")

        if not request or not request.user.retailer_id:
            return value

        queryset = Category.objects.filter(
            retailer=request.user.retailer, name__iexact=value
        )

        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)

        if queryset.exists():
            raise serializers.ValidationError(
                "Category name already exists for this retailer"
            )

        return value

    def validate_code(self, value):

        if not value:
            return value

        value = value.strip().upper()

        request = self.context.get("request")

        if not request or not request.user.retailer_id:
            return value

        queryset = Category.objects.filter(
            retailer=request.user.retailer, code__iexact=value
        )

        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)

        if queryset.exists():
            raise serializers.ValidationError(
                "Category code already exists for this retailer"
            )

        return value

    def validate(self, attrs):

        request = self.context.get("request")

        if request and not request.user.is_superuser:
            user = request.user

            if not user.retailer_id:
                raise serializers.ValidationError("Retailer is required")

            if self.instance and self.instance.retailer_id != user.retailer_id:
                raise serializers.ValidationError(
                    "You cannot modify another retailer's category"
                )

        return attrs

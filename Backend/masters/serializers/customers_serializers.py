from rest_framework import serializers

from masters.models.customers_models import Customer


class CustomerSerializer(serializers.ModelSerializer):

    retailer_name = serializers.CharField(
        source="retailer.name",
        read_only=True
    )

    branch_name = serializers.CharField(
        source="branch.name",
        read_only=True
    )

    class Meta:
        model = Customer

        fields = [
            "id",

            # Retailer Info
            "retailer",
            "retailer_name",

            # Branch Info
            "branch",
            "branch_name",

            # Customer Info
            "name",
            "mobile",
            "email",
            "address",

            # Status
            "is_active",

            # Timestamps
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

    def validate_mobile(self, value):

        queryset = Customer.objects.filter(
            mobile=value
        )

        if self.instance:
            queryset = queryset.exclude(
                id=self.instance.id
            )

        if queryset.exists():
            raise serializers.ValidationError(
                "Customer with this mobile already exists"
            )

        return value
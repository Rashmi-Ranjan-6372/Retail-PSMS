from rest_framework import serializers

from masters.models.customers_models import Customer, RetailerCustomer


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer

        fields = [
            "id",
            "name",
            "mobile",
            "email",
            "address",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_mobile(self, value):

        value = value.strip()

        if self.instance:
            queryset = Customer.objects.filter(mobile=value).exclude(
                id=self.instance.id
            )

            if queryset.exists():
                raise serializers.ValidationError(
                    "Customer with this mobile already exists"
                )

        return value

class RetailerCustomerSerializer(serializers.ModelSerializer):

    customer = CustomerSerializer(read_only=True)

    retailer_name = serializers.CharField(source="retailer.name", read_only=True)

    branch_name = serializers.CharField(
        source="branch.name", read_only=True, allow_null=True
    )

    class Meta:
        model = RetailerCustomer

        fields = [
            "id",
            # Customer Information
            "customer",
            # Retailer Information
            "retailer",
            "retailer_name",
            # Branch Information
            "branch",
            "branch_name",
            # Status
            "is_active",
            # Timestamps
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "customer",
            "retailer",
            "retailer_name",
            "branch",
            "branch_name",
            "created_at",
            "updated_at",
        ]

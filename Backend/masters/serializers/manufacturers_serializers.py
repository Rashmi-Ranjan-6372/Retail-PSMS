from rest_framework import serializers

from masters.models.manufacturers_models import Manufacturer


class ManufacturerSerializer(serializers.ModelSerializer):

    retailer_name = serializers.CharField(source="retailer.name", read_only=True)

    branch_name = serializers.CharField(
        source="branch.name", read_only=True, allow_null=True
    )

    class Meta:
        model = Manufacturer

        fields = [
            "id",
            "retailer",
            "retailer_name",
            "branch",
            "branch_name",
            "name",
            "gst_no",
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

        value = value.strip()

        retailer = (
            self.instance.retailer
            if self.instance
            else self.context["request"].user.retailer
        )

        if retailer is None:
            raise serializers.ValidationError(
                "Retailer is required to validate manufacturer name."
            )

        queryset = Manufacturer.objects.filter(retailer=retailer, name__iexact=value)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "Manufacturer already exists for this retailer."
            )

        return value

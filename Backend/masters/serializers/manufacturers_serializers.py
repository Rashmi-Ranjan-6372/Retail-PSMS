from rest_framework import serializers

from masters.models.manufacturers_models import Manufacturer

class ManufacturerSerializer(serializers.ModelSerializer):

    retailer_name = serializers.CharField(
        source="retailer.name",
        read_only=True
    )

    branch_name = serializers.CharField(
        source="branch.name",
        read_only=True
    )

    class Meta:
        model = Manufacturer

        fields = [
            "id",

            # Retailer Info
            "retailer",
            "retailer_name",

            # Branch Info
            "branch",
            "branch_name",

            # Manufacturer Info
            "name",
            "gst_no",

            # Status
            "is_active",

            # Timestamps
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "id",
            "retailer",
            "branch",
            "retailer_name",
            "branch_name",
            "created_at",
            "updated_at",
        )

    def validate_name(self, value):

        value = value.strip()

        request = self.context.get("request")

        queryset = Manufacturer.objects.filter(
            name__iexact=value
        )

        # ================= RETAILER WISE CHECK =================
        if request and not request.user.is_superuser:
            queryset = queryset.filter(
                retailer=request.user.retailer
            )

        instance = getattr(self, "instance", None)

        if instance:
            queryset = queryset.exclude(
                id=instance.id
            )

        if queryset.exists():
            raise serializers.ValidationError(
                "Manufacturer already exists"
            )

        return value
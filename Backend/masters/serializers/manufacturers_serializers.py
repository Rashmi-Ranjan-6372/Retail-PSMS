from rest_framework import serializers
from masters.models import Manufacturer


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")

    def validate_name(self, value):
        instance = getattr(self, "instance", None)

        queryset = Manufacturer.objects.filter(name__iexact=value)
        if instance:
            queryset = queryset.exclude(id=instance.id)

        if queryset.exists():
            raise serializers.ValidationError("Manufacturer already exists")

        return value
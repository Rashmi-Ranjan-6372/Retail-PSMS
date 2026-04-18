from rest_framework import serializers
from masters.models import Supplier
from branches.models import Branch


class SupplierSerializer(serializers.ModelSerializer):
    branches = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Branch.objects.all(),
        required=False
    )

    class Meta:
        model = Supplier
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")

    def validate(self, data):
        user = self.context["request"].user

        if user.is_superuser:
            if not data.get("branches"):
                raise serializers.ValidationError({
                    "branches": "This field is required for super admin."
                })
        else:
            data.pop("branches", None)

        return data
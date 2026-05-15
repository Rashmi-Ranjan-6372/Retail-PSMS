from rest_framework import serializers
from .models import Branch


class BranchSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField(read_only=True)
    logo_file = serializers.ImageField(
        write_only=True,
        required=False
    )

    class Meta:
        model = Branch

        fields = "__all__"

        read_only_fields = (
            "id",
            "retailer",
            "created_at",
            "updated_at",
            "deleted_at",
            "deleted_by",
        )

    def get_logo(self, obj):
        request = self.context.get("request")

        if obj.logo:
            if request:
                return request.build_absolute_uri(
                    obj.logo.url
                )

            return obj.logo.url

        return None

    def validate_logo_file(self, value):
        max_size = 2 * 1024 * 1024

        if value.size > max_size:
            raise serializers.ValidationError(
                "Logo size must be below 2MB."
            )

        allowed_types = [
            "image/jpeg",
            "image/png",
            "image/webp",
        ]

        if value.content_type not in allowed_types:
            raise serializers.ValidationError(
                "Only JPG, PNG and WEBP images are allowed."
            )

        return value

    def create(self, validated_data):
        logo_file = validated_data.pop(
            "logo_file",
            None
        )

        branch = Branch.objects.create(
            **validated_data
        )

        if logo_file:
            branch.logo = logo_file
            branch.save()

        return branch

    def update(self, instance, validated_data):
        logo_file = validated_data.pop(
            "logo_file",
            None
        )

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if logo_file:
            instance.logo = logo_file

        instance.save()

        return instance
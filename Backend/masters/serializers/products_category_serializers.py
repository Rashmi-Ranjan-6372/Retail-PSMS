from rest_framework import serializers
from masters.models import Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"

    def validate_name(self, value):
        return value.strip().title()

    def validate_code(self, value):
        if value:
            return value.strip().upper()
        return value

    def create(self, validated_data):
        if validated_data.get("code"):
            validated_data["code"] = validated_data["code"].upper()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get("code"):
            validated_data["code"] = validated_data["code"].upper()
        return super().update(instance, validated_data)
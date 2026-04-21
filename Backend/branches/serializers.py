from rest_framework import serializers
from .models import Branch

class BranchSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(required=False)
    class Meta:
        model = Branch
        fields = "__all__"
        read_only_fields = ("id", "created_at")

    def get_logo(self, obj):
        request = self.context.get("request")
        if obj.logo:
            return request.build_absolute_uri(obj.logo.url)
        return None
from rest_framework import serializers
from inventory.models.expiry_damage_models import ExpiryDamage


class ExpiryDamageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExpiryDamage
        fields = "__all__"
        read_only_fields = [
            "total_loss",
            "created_at",
            "updated_at",
        ]
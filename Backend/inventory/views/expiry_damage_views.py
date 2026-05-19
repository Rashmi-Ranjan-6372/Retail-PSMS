from rest_framework.viewsets import ModelViewSet
from inventory.models.expiry_damage_models import ExpiryDamage
from inventory.serializers.expiry_damage_serializers import (
    ExpiryDamageSerializer
)


class ExpiryDamageViewSet(ModelViewSet):

    queryset = ExpiryDamage.objects.all()
    serializer_class = ExpiryDamageSerializer
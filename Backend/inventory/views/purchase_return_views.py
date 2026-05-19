from rest_framework.viewsets import ModelViewSet
from inventory.models.purchase_return_models import (
    PurchaseReturn
)
from inventory.serializers.purchase_return_serializers import (
    PurchaseReturnSerializer
)


class PurchaseReturnViewSet(ModelViewSet):

    queryset = PurchaseReturn.objects.all()
    serializer_class = PurchaseReturnSerializer
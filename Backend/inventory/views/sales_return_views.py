from rest_framework.viewsets import ModelViewSet
from inventory.models.sales_return_models import (
    SalesReturn
)
from inventory.serializers.sales_return_serializers import (
    SalesReturnSerializer
)


class SalesReturnViewSet(ModelViewSet):

    queryset = SalesReturn.objects.all()
    serializer_class = SalesReturnSerializer
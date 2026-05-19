from rest_framework.viewsets import ModelViewSet
from inventory.models.sales_models import Sales
from inventory.serializers.sales_serializers import (
    SalesSerializer
)


class SalesViewSet(ModelViewSet):

    queryset = Sales.objects.all()
    serializer_class = SalesSerializer
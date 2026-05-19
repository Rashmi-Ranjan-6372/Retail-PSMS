from rest_framework.viewsets import ModelViewSet
from inventory.models.receipt_models import Receipt
from inventory.serializers.receipt_serializers import (
    ReceiptSerializer
)


class ReceiptViewSet(ModelViewSet):

    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
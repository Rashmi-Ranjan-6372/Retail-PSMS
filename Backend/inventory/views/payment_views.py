from rest_framework.viewsets import ModelViewSet
from inventory.models.payment_models import Payment
from inventory.serializers.payment_serializers import (
    PaymentSerializer
)


class PaymentViewSet(ModelViewSet):

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
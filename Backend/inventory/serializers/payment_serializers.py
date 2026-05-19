from rest_framework import serializers
from inventory.models.payment_models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = [
            "payment_no",
            "due_amount",
            "status",
            "created_at",
            "updated_at",
        ]
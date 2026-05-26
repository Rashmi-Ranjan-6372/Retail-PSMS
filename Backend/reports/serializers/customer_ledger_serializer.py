from rest_framework import serializers


class CustomerLedgerSerializer(serializers.Serializer):

    customer = serializers.CharField()
    invoice_no = serializers.CharField()
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    due_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    created_at = serializers.DateTimeField()
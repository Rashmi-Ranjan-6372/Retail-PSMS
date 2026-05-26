from rest_framework import serializers


class SupplierLedgerSerializer(serializers.Serializer):

    supplier = serializers.CharField()
    transaction_no = serializers.CharField()
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    created_at = serializers.DateTimeField()
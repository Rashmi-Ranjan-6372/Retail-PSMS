from rest_framework import serializers


class ProductLedgerSerializer(serializers.Serializer):

    transaction_no = serializers.CharField()
    transaction_type = serializers.CharField()
    product = serializers.CharField()
    qty = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    created_at = serializers.DateTimeField()
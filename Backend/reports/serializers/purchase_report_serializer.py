from rest_framework import serializers


class PurchaseReportSerializer(serializers.Serializer):

    transaction_no = serializers.CharField()
    supplier = serializers.CharField()
    branch = serializers.CharField()
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    status = serializers.CharField()
    created_at = serializers.DateTimeField()
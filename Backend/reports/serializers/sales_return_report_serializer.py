from rest_framework import serializers


class SalesReturnReportSerializer(serializers.Serializer):

    return_no = serializers.CharField()
    sales_invoice = serializers.CharField()
    branch = serializers.CharField()
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    refund_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    status = serializers.CharField()
    created_at = serializers.DateTimeField()
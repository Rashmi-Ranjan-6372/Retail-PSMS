from rest_framework import serializers


class SalesReportSerializer(serializers.Serializer):

    invoice_no = serializers.CharField()
    customer = serializers.CharField()
    branch = serializers.CharField()
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    discount = serializers.DecimalField(max_digits=12, decimal_places=2)
    net_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    due_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    payment_status = serializers.CharField()
    created_at = serializers.DateTimeField()
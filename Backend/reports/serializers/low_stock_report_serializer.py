from rest_framework import serializers


class LowStockReportSerializer(serializers.Serializer):

    product = serializers.CharField()
    batch_no = serializers.CharField()
    branch = serializers.CharField()
    available_qty = serializers.IntegerField()
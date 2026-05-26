from rest_framework import serializers


class ExpiryReportSerializer(serializers.Serializer):

    product = serializers.CharField()
    batch_no = serializers.CharField()
    branch = serializers.CharField()
    expiry_date = serializers.DateField()
    available_qty = serializers.IntegerField()
    is_expired = serializers.BooleanField()
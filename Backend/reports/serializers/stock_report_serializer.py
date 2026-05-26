from rest_framework import serializers


class StockReportSerializer(serializers.Serializer):

    product = serializers.CharField()
    batch_no = serializers.CharField()
    branch = serializers.CharField()
    quantity = serializers.IntegerField()
    available_qty = serializers.IntegerField()
    reserved_qty = serializers.IntegerField()
    purchase_price = serializers.DecimalField(max_digits=12, decimal_places=2)
    sale_price = serializers.DecimalField(max_digits=12, decimal_places=2)
    expiry_date = serializers.DateField()
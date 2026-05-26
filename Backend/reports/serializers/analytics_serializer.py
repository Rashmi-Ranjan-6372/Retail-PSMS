from rest_framework import serializers


class AnalyticsSerializer(serializers.Serializer):

    total_sales = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_purchase = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_profit = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_customers = serializers.IntegerField()
    total_suppliers = serializers.IntegerField()
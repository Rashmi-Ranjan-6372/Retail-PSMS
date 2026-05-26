from rest_framework import serializers


class DashboardSerializer(serializers.Serializer):

    total_sales = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_purchase = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_profit = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_stock = serializers.IntegerField()
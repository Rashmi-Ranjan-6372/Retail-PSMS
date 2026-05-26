from rest_framework import serializers


class ProfitLossSerializer(serializers.Serializer):

    branch = serializers.CharField()
    sales = serializers.DecimalField(max_digits=12, decimal_places=2)
    purchase = serializers.DecimalField(max_digits=12, decimal_places=2)
    profit = serializers.DecimalField(max_digits=12, decimal_places=2)
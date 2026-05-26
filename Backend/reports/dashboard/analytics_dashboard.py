from inventory.models.sales_models import Sales
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.db.models.functions import Coalesce


class AnalyticsDashboardService:

    @staticmethod
    def monthly_sales(retailer=None, branch=None):

        queryset = Sales.objects.all()

        if retailer:
            queryset = queryset.filter(retailer=retailer)

        if branch:
            queryset = queryset.filter(branch=branch)

        return queryset.annotate(
            month=TruncMonth("created_at")
        ).values(
            "month"
        ).annotate(
            total_sales=Coalesce(Sum("net_amount"), 0)
        ).order_by("month")
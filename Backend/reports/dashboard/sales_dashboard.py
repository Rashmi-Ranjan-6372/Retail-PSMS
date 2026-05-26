from inventory.models.sales_models import Sales
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce


class SalesDashboardService:

    @staticmethod
    def get_dashboard(retailer=None, branch=None):

        queryset = Sales.objects.all()

        if retailer:
            queryset = queryset.filter(retailer=retailer)

        if branch:
            queryset = queryset.filter(branch=branch)

        return {
            "total_sales": queryset.aggregate(
                total=Coalesce(Sum("net_amount"), 0)
            )["total"],

            "total_invoices": queryset.aggregate(
                total=Coalesce(Count("id"), 0)
            )["total"],

            "paid_sales": queryset.filter(
                payment_status="PAID"
            ).count(),

            "unpaid_sales": queryset.filter(
                payment_status="UNPAID"
            ).count(),
        }
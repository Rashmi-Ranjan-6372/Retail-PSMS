from inventory.models.sales_models import Sales
from inventory.models.stock_batch_models import StockBatch
from inventory.models import StockBatch
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce


class DashboardService:

    @staticmethod
    def get_dashboard():

        return {
            "total_sales": Sales.objects.aggregate(
                total=Coalesce(Sum("net_amount"), 0)
            )["total"],

            "invoice_count": Sales.objects.aggregate(
                count=Count("id")
            )["count"],

            "total_stock": StockBatch.objects.aggregate(
                total=Coalesce(Sum("available_qty"), 0)
            )["total"]
        }
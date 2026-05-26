from inventory.models.stock_batch_models import StockBatch
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils.timezone import now


class StockDashboardService:

    @staticmethod
    def get_dashboard(retailer=None, branch=None):

        queryset = StockBatch.objects.all()

        if retailer:
            queryset = queryset.filter(retailer=retailer)

        if branch:
            queryset = queryset.filter(branch=branch)

        return {

            "total_stock_qty": queryset.aggregate(
                total=Coalesce(Sum("available_qty"), 0)
            )["total"],

            "expired_products": queryset.filter(
                expiry_date__lt=now().date()
            ).count(),

            "low_stock_products": queryset.filter(
                available_qty__lte=10
            ).count(),
        }
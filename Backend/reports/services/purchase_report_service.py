from inventory.models.stock_transaction_models import StockTransaction
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce


class PurchaseReportService:

    @staticmethod
    def get_report():

        queryset = StockTransaction.objects.all()

        summary = queryset.aggregate(
            total_purchase=Coalesce(Sum("net_amount"), 0),
            purchase_count=Count("id")
        )

        return {
            "summary": summary,
            "data": queryset
        }
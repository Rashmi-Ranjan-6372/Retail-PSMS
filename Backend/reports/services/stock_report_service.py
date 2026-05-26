from inventory.models.stock_batch_models import StockBatch
from django.db.models import Sum
from django.db.models.functions import Coalesce


class StockReportService:

    @staticmethod
    def get_report():

        queryset = StockBatch.objects.all()

        summary = queryset.aggregate(
            total_stock=Coalesce(Sum("available_qty"), 0)
        )

        return {
            "summary": summary,
            "data": queryset
        }
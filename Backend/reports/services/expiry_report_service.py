from inventory.models.stock_batch_models import StockBatch
from django.utils.timezone import now


class ExpiryReportService:

    @staticmethod
    def get_report():

        queryset = StockBatch.objects.filter(
            expiry_date__lt=now().date()
        )

        return queryset
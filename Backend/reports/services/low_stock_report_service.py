from inventory.models.stock_batch_models import StockBatch


class LowStockReportService:

    @staticmethod
    def get_report(threshold=10):

        return StockBatch.objects.filter(
            available_qty__lte=threshold
        )
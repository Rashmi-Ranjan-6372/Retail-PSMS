from inventory.models.stock_adjustment_models import StockAdjustment


class StockAdjustmentReportService:

    @staticmethod
    def get_report():

        return StockAdjustment.objects.all()
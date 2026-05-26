from inventory.models.stock_transfer_models import StockTransfer


class StockTransferReportService:

    @staticmethod
    def get_report():

        return StockTransfer.objects.all()
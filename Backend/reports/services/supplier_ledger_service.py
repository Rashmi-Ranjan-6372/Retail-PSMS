from inventory.models.stock_transaction_models import StockTransaction


class SupplierLedgerService:

    @staticmethod
    def get_supplier_ledger(supplier_id):

        return StockTransaction.objects.filter(
            supplier_id=supplier_id
        )
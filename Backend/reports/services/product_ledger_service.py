from inventory.models.stock_transaction_item_models import StockTransactionItem


class ProductLedgerService:

    @staticmethod
    def get_product_ledger(product_id):

        return StockTransactionItem.objects.filter(
            product_id=product_id
        ).order_by("created_at")
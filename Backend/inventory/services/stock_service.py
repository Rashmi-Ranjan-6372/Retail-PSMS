
from inventory.models.stock_batch_models import StockBatch


class StockService:

    @staticmethod
    def get_product_stock(product_id, branch_id=None):

        queryset = StockBatch.objects.filter(
            product_id=product_id
        )

        if branch_id:
            queryset = queryset.filter(
                branch_id=branch_id
            )

        total_stock = sum(
            queryset.values_list(
                "available_qty",
                flat=True
            )
        )

        return total_stock
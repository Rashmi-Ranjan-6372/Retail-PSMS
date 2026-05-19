
from inventory.models.stock_batch_models import StockBatch


class BatchService:

    @staticmethod
    def update_available_qty(batch_id, qty, operation="minus"):

        batch = StockBatch.objects.get(id=batch_id)

        if operation == "minus":
            batch.available_qty -= qty

        elif operation == "plus":
            batch.available_qty += qty

        batch.save()

        return batch
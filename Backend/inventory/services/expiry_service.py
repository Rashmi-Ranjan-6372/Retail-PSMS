
from django.utils.timezone import now
from inventory.models.stock_batch_models import StockBatch


class ExpiryService:

    @staticmethod
    def update_expired_batches():

        batches = StockBatch.objects.filter(
            expiry_date__lt=now().date()
        )

        for batch in batches:
            batch.is_expired = True
            batch.save()

        return batches.count()
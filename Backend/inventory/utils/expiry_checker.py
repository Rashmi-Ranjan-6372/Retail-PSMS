from django.utils.timezone import now
from inventory.models.stock_batch_models import StockBatch


def check_expired_batches():

    expired_batches = StockBatch.objects.filter(
        expiry_date__lt=now().date()
    )

    for batch in expired_batches:

        if not batch.is_expired:
            batch.is_expired = True
            batch.save()

    return expired_batches.count()
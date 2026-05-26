from django.utils.timezone import now
from datetime import timedelta
from inventory.models.stock_batch_models import StockBatch


def get_expiry_alerts(days=30):

    expiry_date = now().date() + timedelta(days=days)

    batches = StockBatch.objects.filter(
        expiry_date__lte=expiry_date,
        is_expired=False,
        available_qty__gt=0
    )

    data = []

    for batch in batches:

        data.append({
            "product": batch.product.name,
            "batch_no": batch.batch_no,
            "expiry_date": batch.expiry_date,
            "available_qty": batch.available_qty
        })

    return data
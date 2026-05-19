
from inventory.models.stock_batch_models import StockBatch


def allocate_batch(product, qty):

    batches = StockBatch.objects.filter(
        product=product,
        available_qty__gt=0,
        is_expired=False
    ).order_by("expiry_date")

    allocated_batches = []

    remaining_qty = qty

    for batch in batches:

        if remaining_qty <= 0:
            break

        take_qty = min(
            batch.available_qty,
            remaining_qty
        )

        allocated_batches.append({
            "batch": batch,
            "qty": take_qty
        })

        remaining_qty -= take_qty

    return allocated_batches
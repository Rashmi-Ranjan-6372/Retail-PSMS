from inventory.models.stock_batch_models import StockBatch


LOW_STOCK_LIMIT = 10


def get_low_stock_alerts():

    batches = StockBatch.objects.filter(
        available_qty__lte=LOW_STOCK_LIMIT
    )

    data = []

    for batch in batches:

        data.append({
            "product": batch.product.name,
            "batch_no": batch.batch_no,
            "available_qty": batch.available_qty
        })

    return data
from django.db import transaction

from inventory.models.stock_batch_models import (
    StockBatch
)


@transaction.atomic
def process_stock_transfer(stock_transfer):

    source_batch = stock_transfer.batch

    transfer_qty = stock_transfer.quantity

    # ==========================================
    # CHECK STOCK
    # ==========================================

    if source_batch.available_qty < transfer_qty:
        raise ValueError(
            "Insufficient stock for transfer"
        )

    # ==========================================
    # REMOVE STOCK FROM SOURCE
    # ==========================================

    source_batch.available_qty -= transfer_qty

    source_batch.save()

    # ==========================================
    # ADD STOCK TO DESTINATION
    # ==========================================

    destination_batch, created = (
        StockBatch.objects.get_or_create(
            retailer=stock_transfer.retailer,
            branch=stock_transfer.to_branch,
            product=stock_transfer.product,
            batch_no=source_batch.batch_no,

            defaults={
                "supplier": source_batch.supplier,
                "quantity": transfer_qty,
                "available_qty": transfer_qty,
                "reserved_qty": 0,
                "purchase_price": source_batch.purchase_price,
                "sale_price": source_batch.sale_price,
                "mrp": source_batch.mrp,
                "expiry_date": source_batch.expiry_date,
                "manufacture_date": source_batch.manufacture_date,
                "created_by": stock_transfer.created_by,
            }
        )
    )

    # ==========================================
    # IF BATCH EXISTS
    # ==========================================

    if not created:

        destination_batch.quantity += transfer_qty

        destination_batch.available_qty += transfer_qty

        destination_batch.save()

    return stock_transfer
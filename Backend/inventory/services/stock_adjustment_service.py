from django.db import transaction

from inventory.models.stock_adjustment_models import (
    StockAdjustment
)

from inventory.models.stock_batch_models import (
    StockBatch
)


# =====================================================
# PROCESS STOCK ADJUSTMENT
# =====================================================

@transaction.atomic
def process_stock_adjustment(
    stock_adjustment
):

    batch = (
        StockBatch.objects
        .select_for_update()
        .get(id=stock_adjustment.batch.id)
    )

    qty = (
        stock_adjustment.adjustment_qty or 0
    )

    # =================================================
    # STOCK INCREASE
    # =================================================

    if stock_adjustment.adjustment_type == "IN":

        batch.available_qty += qty
        batch.quantity += qty

    # =================================================
    # STOCK DECREASE
    # =================================================

    elif stock_adjustment.adjustment_type == "OUT":

        if batch.available_qty < qty:

            raise ValueError(
                f"Insufficient stock for "
                f"{batch.product.name}"
            )

        batch.available_qty -= qty
        batch.quantity -= qty

        if batch.quantity < 0:
            batch.quantity = 0

    batch.save()

    # =================================================
    # UPDATE TOTAL VALUE
    # =================================================

    stock_adjustment.total_value = (
        qty *
        stock_adjustment.unit_price
    )

    stock_adjustment.save()

    return stock_adjustment
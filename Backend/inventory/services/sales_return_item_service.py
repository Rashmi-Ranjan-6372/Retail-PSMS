from django.db import transaction

from inventory.models.stock_batch_models import (
    StockBatch
)

from inventory.models.sales_return_models import (
    SalesReturn
)


# =====================================================
# PROCESS SALES RETURN ITEM
# =====================================================

@transaction.atomic
def process_sales_return_item(
    sales_return_item
):

    batch = sales_return_item.batch

    # =========================
    # RESTORE STOCK
    # =========================

    total_qty = (
        sales_return_item.qty +
        sales_return_item.free_qty
    )

    batch.available_qty += total_qty

    batch.save()

    # =========================
    # UPDATE SALES RETURN TOTAL
    # =========================

    sales_return = (
        sales_return_item.sales_return
    )

    total = 0

    for item in sales_return.items.all():

        total += item.amount

    sales_return.total_amount = total

    sales_return.refund_amount = total

    sales_return.save()
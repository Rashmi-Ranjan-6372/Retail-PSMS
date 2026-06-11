from django.db import transaction
from inventory.models.stock_batch_models import (StockBatch)
from inventory.models.sales_return_models import (SalesReturn)
from subscriptions.utils import (check_subscription_write_access, validate_branch_subscription)


# =====================================================
# PROCESS SALES RETURN ITEM
# =====================================================

@transaction.atomic
def process_sales_return_item(
    sales_return_item
):

    check_subscription_write_access(
        sales_return_item.retailer
    )

    validate_branch_subscription(
        sales_return_item.retailer
    )

    batch = sales_return_item.batch

    # =========================
    # RESTORE STOCK
    # =========================

    total_qty = (
        sales_return_item.qty +
        sales_return_item.free_qty
    )

    batch.available_qty += total_qty

    batch.save(
        update_fields=[
            "available_qty"
        ]
    )

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

    sales_return.save(
        update_fields=[
            "total_amount",
            "refund_amount"
        ]
    )

    return sales_return_item
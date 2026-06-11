from django.db import transaction
from inventory.models.purchase_return_item_models import (PurchaseReturnItem)
from subscriptions.utils import (check_subscription_write_access,validate_branch_subscription)


# =====================================================
# PROCESS PURCHASE RETURN ITEM
# =====================================================

@transaction.atomic
def process_purchase_return_item(purchase_return_item):
    
    check_subscription_write_access(purchase_return_item.retailer)
    validate_branch_subscription(purchase_return_item.retailer)

    batch = purchase_return_item.batch

    # =========================
    # REDUCE STOCK
    # =========================

    total_qty = (
        purchase_return_item.qty +
        purchase_return_item.free_qty
    )

    if batch.available_qty < total_qty:

        raise ValueError(
            "Insufficient stock available."
        )

    batch.available_qty -= total_qty

    batch.save(
        update_fields=[
            "available_qty"
        ]
    )

    # =========================
    # UPDATE PURCHASE RETURN TOTAL
    # =========================

    purchase_return = (
        purchase_return_item.purchase_return
    )

    total = 0

    for item in purchase_return.items.all():

        total += item.amount

    purchase_return.total_amount = total

    purchase_return.adjusted_amount = total

    purchase_return.save(
        update_fields=[
            "total_amount",
            "adjusted_amount"
        ]
    )

    return purchase_return_item
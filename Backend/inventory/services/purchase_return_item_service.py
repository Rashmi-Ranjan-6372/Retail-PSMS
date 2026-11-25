from django.db import transaction
from django.db.models import Sum, DecimalField
from django.db.models.functions import Coalesce

from inventory.models.purchase_return_item_models import PurchaseReturnItem
from inventory.models.stock_batch_models import StockBatch
from inventory.models.purchase_return_models import PurchaseReturn

from subscriptions.utils import (
    check_subscription_write_access,
    validate_branch_subscription,
)

# =====================================================
# PROCESS PURCHASE RETURN ITEM
# =====================================================


@transaction.atomic
def process_purchase_return_item(purchase_return_item):

    # =========================
    # LOCK PURCHASE RETURN ITEM
    # =========================

    try:
        purchase_return_item = (
            PurchaseReturnItem.objects.select_for_update()
            .select_related("retailer", "branch")
            .get(id=purchase_return_item.id)
        )
    except PurchaseReturnItem.DoesNotExist:
        raise ValueError("Purchase return item not found.")

    retailer = purchase_return_item.retailer

    check_subscription_write_access(retailer)
    validate_branch_subscription(retailer)

    # =========================
    # LOCK PURCHASE RETURN
    # =========================

    try:
        purchase_return = PurchaseReturn.objects.select_for_update().get(
            id=purchase_return_item.purchase_return_id
        )
    except PurchaseReturn.DoesNotExist:
        raise ValueError("Purchase return not found.")

    if purchase_return.retailer_id != retailer.id:
        raise ValueError("Purchase return does not belong to this retailer.")

    # =========================
    # LOCK STOCK BATCH
    # =========================

    try:
        batch = StockBatch.objects.select_for_update().get(
            id=purchase_return_item.batch_id
        )
    except StockBatch.DoesNotExist:
        raise ValueError("Stock batch not found.")

    if batch.retailer_id != retailer.id:
        raise ValueError("Stock batch does not belong to this retailer.")

    if batch.product_id != purchase_return_item.product_id:
        raise ValueError("Stock batch does not belong to the selected product.")

    if batch.branch_id != purchase_return_item.branch_id:
        raise ValueError("Stock batch does not belong to the selected branch.")

    if purchase_return_item.branch_id != purchase_return.branch_id:
        raise ValueError(
            "Purchase return item branch does not match purchase return branch."
        )

    # =========================
    # VALIDATE QUANTITY
    # =========================

    total_qty = purchase_return_item.qty + purchase_return_item.free_qty

    if total_qty <= 0:
        raise ValueError("Purchase return quantity must be greater than 0.")

    if batch.available_qty < total_qty:
        raise ValueError("Insufficient available stock for purchase return.")

    if batch.quantity < total_qty:
        raise ValueError("Purchase return quantity exceeds total batch stock.")

    # =========================
    # REDUCE STOCK
    # =========================

    batch.available_qty -= total_qty
    batch.quantity -= total_qty

    batch.save(update_fields=["available_qty", "quantity"])

    # =========================
    # UPDATE PURCHASE RETURN TOTAL
    # =========================

    total = PurchaseReturnItem.objects.filter(
        purchase_return=purchase_return
    ).aggregate(
        total=Coalesce(
            Sum("amount"), 0, output_field=DecimalField(max_digits=14, decimal_places=2)
        )
    )[
        "total"
    ]

    purchase_return.total_amount = total
    purchase_return.adjusted_amount = total

    purchase_return.save(
        update_fields=["total_amount", "adjusted_amount", "updated_at"]
    )

    return purchase_return_item

from decimal import Decimal

from django.db import transaction
from django.db.models import Sum, DecimalField
from django.db.models.functions import Coalesce

from inventory.models.stock_batch_models import StockBatch
from inventory.models.sales_return_models import SalesReturn
from inventory.models.sales_return_item_models import SalesReturnItem

from subscriptions.utils import (
    check_subscription_write_access,
    validate_branch_subscription,
)

# =====================================================
# PROCESS SALES RETURN ITEM
# =====================================================


@transaction.atomic
def process_sales_return_item(sales_return_item):

    # =========================
    # LOCK SALES RETURN ITEM
    # =========================

    try:
        sales_return_item = (
            SalesReturnItem.objects.select_for_update()
            .select_related("retailer", "branch")
            .get(id=sales_return_item.id)
        )
    except SalesReturnItem.DoesNotExist:
        raise ValueError("Sales return item not found.")

    retailer = sales_return_item.retailer

    check_subscription_write_access(retailer)
    validate_branch_subscription(retailer)

    # =========================
    # LOCK SALES RETURN
    # =========================

    try:
        sales_return = SalesReturn.objects.select_for_update().get(
            id=sales_return_item.sales_return_id
        )
    except SalesReturn.DoesNotExist:
        raise ValueError("Sales return not found.")

    if sales_return.retailer_id != retailer.id:
        raise ValueError("Sales return does not belong to this retailer.")

    if sales_return.branch_id != sales_return_item.branch_id:
        raise ValueError("Sales return item branch does not match sales return branch.")

    # =========================
    # LOCK STOCK BATCH
    # =========================

    try:
        batch = StockBatch.objects.select_for_update().get(
            id=sales_return_item.batch_id
        )
    except StockBatch.DoesNotExist:
        raise ValueError("Stock batch not found.")

    if batch.retailer_id != retailer.id:
        raise ValueError("Stock batch does not belong to this retailer.")

    if batch.branch_id != sales_return_item.branch_id:
        raise ValueError("Stock batch does not belong to this branch.")

    if batch.product_id != sales_return_item.product_id:
        raise ValueError("Stock batch does not belong to the selected product.")

    # =========================
    # VALIDATE QUANTITY
    # =========================

    total_qty = sales_return_item.qty + sales_return_item.free_qty

    if total_qty <= 0:
        raise ValueError("Return quantity must be greater than 0.")

    # =========================
    # CHECK RETURN CONDITION
    # =========================

    if sales_return_item.return_condition != "RESELLABLE":
        raise ValueError(
            "Only resalable returned items can be added to available stock."
        )

    # =========================
    # RESTORE STOCK
    # =========================

    if batch.available_qty + batch.reserved_qty + total_qty > batch.quantity:
        batch.quantity += total_qty

    batch.available_qty += total_qty

    batch.save(update_fields=["quantity", "available_qty", "updated_at"])

    # =========================
    # UPDATE SALES RETURN TOTAL
    # =========================

    totals = SalesReturnItem.objects.filter(sales_return=sales_return).aggregate(
        total_amount=Coalesce(
            Sum("amount"),
            Decimal("0.00"),
            output_field=DecimalField(max_digits=14, decimal_places=2),
        )
    )

    total = Decimal(str(totals["total_amount"]))

    sales_return.total_amount = total

    sales_return.refund_amount = min(
        Decimal(str(sales_return.refund_amount or 0)), total
    )

    sales_return.save(update_fields=["total_amount", "refund_amount", "updated_at"])

    return sales_return_item

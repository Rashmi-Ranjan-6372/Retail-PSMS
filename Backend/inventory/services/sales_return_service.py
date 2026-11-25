from decimal import Decimal

from django.db import transaction

from inventory.models.sales_models import Sales
from inventory.models.sales_return_models import SalesReturn
from inventory.models.sales_return_item_models import SalesReturnItem
from inventory.models.stock_batch_models import StockBatch

from subscriptions.utils import (
    check_subscription_write_access,
    validate_branch_subscription,
)

# =====================================================
# PROCESS SALES RETURN
# =====================================================


@transaction.atomic
def process_sales_return(sales_return_id):

    # =====================================================
    # LOCK SALES RETURN
    # =====================================================

    try:
        sales_return = SalesReturn.objects.select_for_update().get(id=sales_return_id)
    except SalesReturn.DoesNotExist:
        raise ValueError("Sales return not found.")

    check_subscription_write_access(sales_return.retailer)

    validate_branch_subscription(sales_return.retailer)

    # =====================================================
    # PREVENT DOUBLE PROCESSING
    # =====================================================

    if sales_return.status == "COMPLETED":
        raise ValueError("Sales return already processed.")

    # =====================================================
    # LOCK ORIGINAL SALES
    # =====================================================

    try:
        sales = Sales.objects.select_for_update().get(id=sales_return.sales_id)
    except Sales.DoesNotExist:
        raise ValueError("Original sales invoice not found.")

    if sales.retailer_id != sales_return.retailer_id:
        raise ValueError("Sales invoice does not belong to this retailer.")

    if sales.branch_id != sales_return.branch_id:
        raise ValueError(
            "Sales return branch does not match the original sales branch."
        )

    # =====================================================
    # LOCK RETURN ITEMS
    # =====================================================

    items = list(
        SalesReturnItem.objects.select_for_update()
        .filter(sales_return=sales_return)
        .order_by("id")
    )

    if not items:
        raise ValueError("Cannot process a sales return without items.")

    total_return_amount = Decimal("0.00")

    # =====================================================
    # PROCESS EACH ITEM
    # =====================================================

    for item in items:

        if item.retailer_id != sales_return.retailer_id:
            raise ValueError("Return item does not belong to this retailer.")

        if item.branch_id != sales_return.branch_id:
            raise ValueError(
                "Return item branch does not match the sales return branch."
            )

        if item.qty <= 0 and item.free_qty <= 0:
            raise ValueError("Return quantity must be greater than zero.")

        return_qty = item.qty + item.free_qty

        # =============================================
        # LOCK STOCK BATCH
        # =============================================

        try:
            batch = StockBatch.objects.select_for_update().get(id=item.batch_id)
        except StockBatch.DoesNotExist:
            raise ValueError(f"Stock batch not found for return item {item.id}.")

        # =============================================
        # VALIDATE BATCH OWNERSHIP
        # =============================================

        if batch.retailer_id != item.retailer_id:
            raise ValueError("Stock batch does not belong to this retailer.")

        if batch.branch_id != item.branch_id:
            raise ValueError("Stock batch does not belong to this branch.")

        if batch.product_id != item.product_id:
            raise ValueError("Stock batch does not belong to the selected product.")

        # =============================================
        # RESTORE RESELLABLE STOCK ONLY
        # =============================================

        if item.return_condition == "RESELLABLE":

            batch.quantity += return_qty
            batch.available_qty += return_qty

            batch.save(update_fields=["quantity", "available_qty", "updated_at"])

        # =============================================
        # CALCULATE RETURN AMOUNT
        # =============================================

        total_return_amount += Decimal(str(item.amount or 0))

    # =====================================================
    # UPDATE SALES RETURN
    # =====================================================

    sales_return.total_amount = total_return_amount
    sales_return.status = "COMPLETED"

    sales_return.save(update_fields=["total_amount", "status"])

    # =====================================================
    # UPDATE ORIGINAL SALES TOTAL
    # =====================================================

    sales_total = Decimal(str(sales.total_amount or 0))

    sales.discount = Decimal(str(sales.discount or 0))

    sales.paid_amount = Decimal(str(sales.paid_amount or 0))

    sales.total_amount = max(Decimal("0.00"), sales_total - total_return_amount)

    # =====================================================
    # RECALCULATE NET AMOUNT
    # =====================================================

    sales.net_amount = max(Decimal("0.00"), sales.total_amount - sales.discount)

    # =====================================================
    # RECALCULATE DUE AMOUNT
    # =====================================================

    sales.due_amount = max(Decimal("0.00"), sales.net_amount - sales.paid_amount)

    # =====================================================
    # UPDATE PAYMENT STATUS
    # =====================================================

    if sales.due_amount == 0:

        sales.payment_status = "PAID"

    elif sales.paid_amount > 0:

        sales.payment_status = "PARTIAL"

    else:

        sales.payment_status = "UNPAID"

    sales.save(
        update_fields=["total_amount", "net_amount", "due_amount", "payment_status"]
    )

    return sales_return

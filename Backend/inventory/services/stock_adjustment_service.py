from decimal import Decimal, InvalidOperation

from django.db import transaction

from inventory.models.stock_adjustment_models import StockAdjustment
from inventory.models.stock_batch_models import StockBatch

from subscriptions.utils import (
    check_subscription_write_access,
    validate_branch_subscription,
)

from accounts.views import create_audit_log

# =====================================================
# PROCESS STOCK ADJUSTMENT
# =====================================================


@transaction.atomic
def process_stock_adjustment(stock_adjustment, request=None):

    # =====================================================
    # LOCK STOCK ADJUSTMENT
    # =====================================================

    try:
        stock_adjustment = StockAdjustment.objects.select_for_update().get(
            id=stock_adjustment.id
        )
    except StockAdjustment.DoesNotExist:
        raise ValueError("Stock adjustment not found.")

    # =====================================================
    # PREVENT DUPLICATE PROCESSING
    # =====================================================

    if stock_adjustment.is_processed:
        raise ValueError("Stock adjustment has already been processed.")

    # =====================================================
    # SUBSCRIPTION VALIDATION
    # =====================================================

    if not stock_adjustment.created_by.is_superuser:

        check_subscription_write_access(stock_adjustment.retailer)

        validate_branch_subscription(stock_adjustment.branch)

    # =====================================================
    # LOCK STOCK BATCH
    # =====================================================

    try:
        batch = (
            StockBatch.objects.select_for_update()
            .select_related("product")
            .get(id=stock_adjustment.batch_id, retailer=stock_adjustment.retailer)
        )
    except StockBatch.DoesNotExist:
        raise ValueError("Stock batch not found for this retailer.")

    # =====================================================
    # VALIDATE OWNERSHIP
    # =====================================================

    if batch.branch_id != stock_adjustment.branch_id:
        raise ValueError("Stock batch does not belong to this branch.")

    if batch.product_id != stock_adjustment.product_id:
        raise ValueError("Stock batch does not belong to the selected product.")

    # =====================================================
    # VALIDATE QUANTITY
    # =====================================================

    try:
        qty = int(stock_adjustment.adjustment_qty)
    except (TypeError, ValueError):
        raise ValueError("Adjustment quantity must be a valid integer.")

    if qty <= 0:
        raise ValueError("Adjustment quantity must be greater than zero.")

    # =====================================================
    # VALIDATE UNIT PRICE
    # =====================================================

    try:
        unit_price = Decimal(str(stock_adjustment.unit_price or 0))
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError("Invalid adjustment unit price.")

    if not unit_price.is_finite() or unit_price < 0:
        raise ValueError("Adjustment unit price cannot be negative or invalid.")

    # =====================================================
    # OLD STOCK VALUES
    # =====================================================

    old_available_qty = batch.available_qty
    old_quantity = batch.quantity

    # =====================================================
    # STOCK INCREASE
    # =====================================================

    if stock_adjustment.adjustment_type == "IN":

        batch.quantity += qty
        batch.available_qty += qty

    # =====================================================
    # STOCK DECREASE
    # =====================================================

    elif stock_adjustment.adjustment_type == "OUT":

        if batch.available_qty < qty:
            raise ValueError(
                f"Insufficient available stock for " f"{batch.product.name}."
            )

        batch.quantity -= qty
        batch.available_qty -= qty

    else:
        raise ValueError("Invalid stock adjustment type. Use IN or OUT.")

    # =====================================================
    # SAVE STOCK BATCH
    # =====================================================

    batch.save(update_fields=["quantity", "available_qty", "updated_at"])

    # =====================================================
    # UPDATE ADJUSTMENT VALUE
    # =====================================================

    stock_adjustment.total_value = Decimal(qty) * unit_price

    stock_adjustment.is_processed = True

    stock_adjustment.save(update_fields=["total_value", "is_processed", "updated_at"])

    # =====================================================
    # AUDIT LOG
    # =====================================================

    if request:

        create_audit_log(
            user=request.user,
            action="create",
            model_name="StockAdjustment",
            object_id=stock_adjustment.id,
            description=(
                f"Stock Adjustment "
                f"{stock_adjustment.adjustment_type} | "
                f"Product: {batch.product.name} | "
                f"Qty: {qty} | "
                f"Available: {old_available_qty}"
                f"->{batch.available_qty} | "
                f"Total: {old_quantity}"
                f"->{batch.quantity}"
            ),
            request=request,
        )

    return stock_adjustment

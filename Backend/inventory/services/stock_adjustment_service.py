from django.db import transaction
from inventory.models.stock_adjustment_models import StockAdjustment
from inventory.models.stock_batch_models import StockBatch
from subscriptions.utils import check_subscription_write_access, validate_branch_subscription
from accounts.views import create_audit_log

# =====================================================
# PROCESS STOCK ADJUSTMENT
# =====================================================

@transaction.atomic
def process_stock_adjustment(
    stock_adjustment,
    request=None
):

    if not stock_adjustment.created_by.is_superuser:
        check_subscription_write_access(
            stock_adjustment.retailer
        )
        validate_branch_subscription(
            stock_adjustment.branch
        )

    batch = (
        StockBatch.objects
        .select_for_update()
        .get(id=stock_adjustment.batch.id)
    )

    qty = (
        stock_adjustment.adjustment_qty or 0
    )

    old_available_qty = batch.available_qty
    old_quantity = batch.quantity

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

    # =================================================
    # AUDIT LOG
    # =================================================

    if request:

        create_audit_log(
            user=request.user,
            action="create",
            model_name="StockAdjustment",
            object_id=stock_adjustment.id,
            description=(
                f"Stock Adjustment "
                f"{stock_adjustment.adjustment_type} | "
                f"Product:{batch.product.name} | "
                f"Qty:{qty} | "
                f"Available:{old_available_qty}->{batch.available_qty} | "
                f"Total:{old_quantity}->{batch.quantity}"
            ),
            request=request
        )

    return stock_adjustment
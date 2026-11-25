from decimal import Decimal, InvalidOperation

from django.db import transaction

from inventory.models.stock_transfer_models import StockTransfer
from inventory.models.stock_batch_models import StockBatch

from subscriptions.utils import (
    check_subscription_write_access,
    validate_branch_subscription,
)

from accounts.views import create_audit_log

# =====================================================
# PROCESS STOCK TRANSFER
# =====================================================


@transaction.atomic
def process_stock_transfer(stock_transfer_id, request=None):

    # =====================================================
    # LOCK STOCK TRANSFER
    # =====================================================

    try:
        stock_transfer = (
            StockTransfer.objects.select_for_update()
            .select_related(
                "product",
                "batch",
                "from_branch",
                "to_branch",
                "retailer",
                "created_by",
            )
            .get(id=stock_transfer_id)
        )
    except StockTransfer.DoesNotExist:
        raise ValueError("Stock transfer not found.")

    # =====================================================
    # PREVENT DOUBLE PROCESSING
    # =====================================================

    if stock_transfer.status == "COMPLETED":
        raise ValueError("Stock transfer already processed.")

    # =====================================================
    # VALIDATE BRANCHES
    # =====================================================

    retailer = stock_transfer.retailer
    source_branch = stock_transfer.from_branch
    destination_branch = stock_transfer.to_branch

    if source_branch.id == destination_branch.id:
        raise ValueError("Source and destination branches cannot be the same.")

    if (
        source_branch.retailer_id != retailer.id
        or destination_branch.retailer_id != retailer.id
    ):
        raise ValueError("Both branches must belong to the same retailer.")

    # =====================================================
    # SUBSCRIPTION VALIDATION
    # =====================================================

    if not stock_transfer.created_by.is_superuser:

        check_subscription_write_access(retailer)

        validate_branch_subscription(source_branch)

        validate_branch_subscription(destination_branch)

    # =====================================================
    # VALIDATE TRANSFER QUANTITY
    # =====================================================

    try:
        transfer_qty = int(stock_transfer.quantity)
    except (TypeError, ValueError):
        raise ValueError("Transfer quantity must be a valid integer.")

    if transfer_qty <= 0:
        raise ValueError("Transfer quantity must be greater than zero.")

    # =====================================================
    # VALIDATE UNIT COST
    # =====================================================

    try:
        unit_cost = Decimal(str(stock_transfer.unit_cost))
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError("Invalid transfer unit cost.")

    if not unit_cost.is_finite() or unit_cost < 0:
        raise ValueError("Transfer unit cost cannot be negative or invalid.")

    # =====================================================
    # LOCK SOURCE BATCH
    # =====================================================

    try:
        source_batch = (
            StockBatch.objects.select_for_update()
            .select_related("product")
            .get(id=stock_transfer.batch_id, retailer=retailer)
        )
    except StockBatch.DoesNotExist:
        raise ValueError("Source stock batch not found.")

    # =====================================================
    # VALIDATE SOURCE BATCH
    # =====================================================

    if source_batch.branch_id != source_branch.id:
        raise ValueError("Stock batch does not belong to the source branch.")

    if source_batch.product_id != stock_transfer.product_id:
        raise ValueError("Stock batch does not belong to the selected product.")

    # =====================================================
    # CHECK AVAILABLE STOCK
    # =====================================================

    if source_batch.available_qty < transfer_qty:
        raise ValueError(
            f"Insufficient available stock for " f"{source_batch.product.name}."
        )

    old_source_available = source_batch.available_qty
    old_source_quantity = source_batch.quantity

    # =====================================================
    # FIND OR CREATE DESTINATION BATCH
    # =====================================================

    destination_batch, created = StockBatch.objects.select_for_update().get_or_create(
        retailer=retailer,
        branch=destination_branch,
        product=source_batch.product,
        batch_no=source_batch.batch_no,
        defaults={
            "supplier": source_batch.supplier,
            "quantity": 0,
            "available_qty": 0,
            "reserved_qty": 0,
            "purchase_price": source_batch.purchase_price,
            "sale_price": source_batch.sale_price,
            "mrp": source_batch.mrp,
            "expiry_date": source_batch.expiry_date,
            "manufacture_date": source_batch.manufacture_date,
            "is_expired": source_batch.is_expired,
            "created_by": stock_transfer.created_by,
        },
    )

    # =====================================================
    # VALIDATE DESTINATION BATCH
    # =====================================================

    if destination_batch.branch_id != destination_branch.id:
        raise ValueError("Destination batch does not belong to the destination branch.")

    if destination_batch.product_id != source_batch.product_id:
        raise ValueError("Destination batch product does not match source batch.")

    if destination_batch.expiry_date != source_batch.expiry_date:
        raise ValueError("Destination batch expiry date does not match source batch.")

    if destination_batch.manufacture_date != source_batch.manufacture_date:
        raise ValueError(
            "Destination batch manufacture date does not match source batch."
        )

    old_destination_available = destination_batch.available_qty
    old_destination_quantity = destination_batch.quantity

    # =====================================================
    # DEDUCT STOCK FROM SOURCE
    # =====================================================

    source_batch.quantity -= transfer_qty
    source_batch.available_qty -= transfer_qty

    source_batch.save(update_fields=["quantity", "available_qty", "updated_at"])

    # =====================================================
    # ADD STOCK TO DESTINATION
    # =====================================================

    destination_batch.quantity += transfer_qty
    destination_batch.available_qty += transfer_qty

    destination_batch.save(update_fields=["quantity", "available_qty", "updated_at"])

    # =====================================================
    # UPDATE TRANSFER VALUE
    # =====================================================

    stock_transfer.total_cost = Decimal(transfer_qty) * unit_cost

    # =====================================================
    # UPDATE TRANSFER STATUS
    # =====================================================

    stock_transfer.status = "COMPLETED"

    stock_transfer.save(update_fields=["total_cost", "status", "updated_at"])

    # =====================================================
    # AUDIT LOG
    # =====================================================

    if request:

        create_audit_log(
            user=request.user,
            action="update",
            model_name="StockTransfer",
            object_id=stock_transfer.id,
            description=(
                f"Transferred {transfer_qty} units of "
                f"{stock_transfer.product.name} "
                f"from {source_branch.name} "
                f"to {destination_branch.name}. "
                f"Source Available: "
                f"{old_source_available}->{source_batch.available_qty}, "
                f"Source Total: "
                f"{old_source_quantity}->{source_batch.quantity}, "
                f"Destination Available: "
                f"{old_destination_available}->{destination_batch.available_qty}, "
                f"Destination Total: "
                f"{old_destination_quantity}->{destination_batch.quantity}"
            ),
            request=request,
        )

    return stock_transfer

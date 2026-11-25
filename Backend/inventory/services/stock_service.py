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
def process_stock_transfer(stock_transfer, request=None):

    # =====================================================
    # LOCK STOCK TRANSFER
    # =====================================================

    try:
        stock_transfer = StockTransfer.objects.select_for_update().get(
            id=stock_transfer.id
        )
    except StockTransfer.DoesNotExist:
        raise ValueError("Stock transfer not found.")

    # =====================================================
    # PREVENT DUPLICATE PROCESSING
    # =====================================================

    if stock_transfer.is_processed:
        raise ValueError("Stock transfer has already been processed.")

    # =====================================================
    # SUBSCRIPTION VALIDATION
    # =====================================================

    if not stock_transfer.created_by.is_superuser:

        check_subscription_write_access(stock_transfer.retailer)

        validate_branch_subscription(stock_transfer.from_branch)

        validate_branch_subscription(stock_transfer.to_branch)

    # =====================================================
    # VALIDATE BRANCHES
    # =====================================================

    if stock_transfer.from_branch_id == stock_transfer.to_branch_id:
        raise ValueError("Source and destination branches cannot be the same.")

    if stock_transfer.from_branch.retailer_id != stock_transfer.retailer_id:
        raise ValueError("Source branch does not belong to this retailer.")

    if stock_transfer.to_branch.retailer_id != stock_transfer.retailer_id:
        raise ValueError("Destination branch does not belong to this retailer.")

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
    # LOCK SOURCE BATCH
    # =====================================================

    try:
        source_batch = (
            StockBatch.objects.select_for_update()
            .select_related("product")
            .get(id=stock_transfer.batch_id, retailer=stock_transfer.retailer)
        )
    except StockBatch.DoesNotExist:
        raise ValueError("Source stock batch not found.")

    # =====================================================
    # VALIDATE SOURCE BATCH
    # =====================================================

    if source_batch.branch_id != stock_transfer.from_branch_id:
        raise ValueError("Stock batch does not belong to the source branch.")

    if source_batch.product_id != stock_transfer.product_id:
        raise ValueError("Stock batch does not belong to the selected product.")

    if source_batch.quantity < transfer_qty:
        raise ValueError("Insufficient total stock for transfer.")

    if source_batch.available_qty < transfer_qty:
        raise ValueError(
            f"Insufficient available stock for " f"{source_batch.product.name}."
        )

    # =====================================================
    # STORE OLD SOURCE STOCK
    # =====================================================

    old_source_available = source_batch.available_qty
    old_source_quantity = source_batch.quantity

    # =====================================================
    # REMOVE STOCK FROM SOURCE
    # =====================================================

    source_batch.quantity -= transfer_qty
    source_batch.available_qty -= transfer_qty

    source_batch.save(update_fields=["quantity", "available_qty", "updated_at"])

    # =====================================================
    # GET OR CREATE DESTINATION BATCH
    # =====================================================

    destination_batch, created = StockBatch.objects.select_for_update().get_or_create(
        retailer=stock_transfer.retailer,
        branch=stock_transfer.to_branch,
        product=source_batch.product,
        batch_no=source_batch.batch_no,
        defaults={
            "supplier": source_batch.supplier,
            "quantity": transfer_qty,
            "available_qty": transfer_qty,
            "reserved_qty": 0,
            "purchase_price": source_batch.purchase_price,
            "sale_price": source_batch.sale_price,
            "mrp": source_batch.mrp,
            "expiry_date": source_batch.expiry_date,
            "manufacture_date": source_batch.manufacture_date,
            "created_by": stock_transfer.created_by,
        },
    )

    # =====================================================
    # STORE OLD DESTINATION STOCK
    # =====================================================

    old_destination_available = 0 if created else destination_batch.available_qty

    old_destination_quantity = 0 if created else destination_batch.quantity

    # =====================================================
    # VALIDATE EXISTING DESTINATION BATCH
    # =====================================================

    if not created:

        if destination_batch.expiry_date != source_batch.expiry_date:
            raise ValueError("Destination batch has a different expiry date.")

        if destination_batch.manufacture_date != source_batch.manufacture_date:
            raise ValueError("Destination batch has a different manufacture date.")

        if destination_batch.purchase_price != source_batch.purchase_price:
            raise ValueError("Destination batch has a different purchase price.")

        if destination_batch.mrp != source_batch.mrp:
            raise ValueError("Destination batch has a different MRP.")

        # =============================================
        # ADD STOCK TO EXISTING DESTINATION BATCH
        # =============================================

        destination_batch.quantity += transfer_qty
        destination_batch.available_qty += transfer_qty

        destination_batch.save(
            update_fields=["quantity", "available_qty", "updated_at"]
        )

    # =====================================================
    # MARK TRANSFER AS PROCESSED
    # =====================================================

    stock_transfer.is_processed = True

    stock_transfer.save(update_fields=["is_processed", "updated_at"])

    # =====================================================
    # AUDIT LOG
    # =====================================================

    if request:

        create_audit_log(
            user=request.user,
            action="create",
            model_name="StockTransfer",
            object_id=stock_transfer.id,
            description=(
                f"Transferred {transfer_qty} units of "
                f"{source_batch.product.name} "
                f"from {stock_transfer.from_branch.name} "
                f"to {stock_transfer.to_branch.name}. "
                f"Source Available: "
                f"{old_source_available}"
                f"->{source_batch.available_qty}, "
                f"Source Total: "
                f"{old_source_quantity}"
                f"->{source_batch.quantity}, "
                f"Destination Available: "
                f"{old_destination_available}"
                f"->{destination_batch.available_qty}, "
                f"Destination Total: "
                f"{old_destination_quantity}"
                f"->{destination_batch.quantity}"
            ),
            request=request,
        )

    return stock_transfer

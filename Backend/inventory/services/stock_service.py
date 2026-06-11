from django.db import transaction
from inventory.models.stock_batch_models import StockBatch
from subscriptions.utils import check_subscription_write_access, validate_branch_subscription
from accounts.views import create_audit_log

@transaction.atomic
def process_stock_transfer(
    stock_transfer,
    request=None
):

    if not stock_transfer.created_by.is_superuser:
        check_subscription_write_access(
            stock_transfer.retailer
        )
        validate_branch_subscription(
            stock_transfer.branch
        )

    source_batch = (
        StockBatch.objects
        .select_for_update()
        .get(id=stock_transfer.batch.id)
    )

    transfer_qty = stock_transfer.quantity

    old_source_available = source_batch.available_qty

    # ==========================================
    # CHECK STOCK
    # ==========================================

    if source_batch.available_qty < transfer_qty:
        raise ValueError(
            "Insufficient stock for transfer"
        )

    # ==========================================
    # REMOVE STOCK FROM SOURCE
    # ==========================================

    source_batch.available_qty -= transfer_qty

    source_batch.save(
        update_fields=["available_qty"]
    )

    # ==========================================
    # ADD STOCK TO DESTINATION
    # ==========================================

    destination_batch, created = (
        StockBatch.objects
        .select_for_update()
        .get_or_create(
            retailer=stock_transfer.retailer,
            branch=stock_transfer.to_branch,
            product=stock_transfer.product,
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
            }
        )
    )

    old_destination_available = (
        destination_batch.available_qty
        if not created else 0
    )

    # ==========================================
    # IF BATCH EXISTS
    # ==========================================

    if not created:

        destination_batch.quantity += transfer_qty

        destination_batch.available_qty += transfer_qty

        destination_batch.save(
            update_fields=[
                "quantity",
                "available_qty"
            ]
        )

    # ==========================================
    # AUDIT LOG
    # ==========================================

    if request:

        create_audit_log(
            user=request.user,
            action="create",
            model_name="StockTransfer",
            object_id=stock_transfer.id,
            description=(
                f"Transferred {transfer_qty} of "
                f"{stock_transfer.product.name} "
                f"from {stock_transfer.from_branch.name} "
                f"to {stock_transfer.to_branch.name}. "
                f"Source Stock:{old_source_available}->{source_batch.available_qty}, "
                f"Destination Stock:{old_destination_available}->{destination_batch.available_qty}"
            ),
            request=request
        )

    return stock_transfer
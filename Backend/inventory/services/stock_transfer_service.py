from decimal import Decimal
from django.db import transaction
from inventory.models.stock_transfer_models import StockTransfer
from inventory.models.stock_batch_models import StockBatch
from subscriptions.utils import check_subscription_write_access, validate_branch_subscription
from accounts.views import create_audit_log

# =====================================================
# PROCESS STOCK TRANSFER
# =====================================================

@transaction.atomic
def process_stock_transfer(
    stock_transfer_id,
    request=None
):

    stock_transfer = (
        StockTransfer.objects
        .select_for_update()
        .select_related(
            "product",
            "batch",
            "from_branch",
            "to_branch",
            "retailer",
        )
        .get(id=stock_transfer_id)
    )

    if not stock_transfer.created_by.is_superuser:
        check_subscription_write_access(
            stock_transfer.retailer
        )
        validate_branch_subscription(
            stock_transfer.branch
        )

    # =====================================================
    # PREVENT DOUBLE PROCESSING
    # =====================================================

    if stock_transfer.status == "COMPLETED":

        raise ValueError(
            "Stock transfer already processed"
        )

    source_batch = (
        StockBatch.objects
        .select_for_update()
        .get(id=stock_transfer.batch.id)
    )

    transfer_qty = stock_transfer.quantity

    old_source_available = source_batch.available_qty

    # =====================================================
    # STOCK VALIDATION
    # =====================================================

    if source_batch.available_qty < transfer_qty:

        raise ValueError(
            f"Insufficient stock for "
            f"{source_batch.product.name}"
        )

    # =====================================================
    # DEDUCT STOCK FROM SOURCE
    # =====================================================

    source_batch.available_qty -= transfer_qty

    source_batch.save(
        update_fields=["available_qty"]
    )

    # =====================================================
    # FIND DESTINATION BATCH
    # =====================================================

    destination_batch, created = (
        StockBatch.objects
        .select_for_update()
        .get_or_create(
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
                "is_expired": source_batch.is_expired,
                "created_by": stock_transfer.created_by,
            }
        )
    )

    old_destination_available = (
        destination_batch.available_qty
        if not created else 0
    )

    # =====================================================
    # UPDATE DESTINATION STOCK
    # =====================================================

    if not created:

        destination_batch.quantity += transfer_qty

        destination_batch.available_qty += transfer_qty

        destination_batch.save(
            update_fields=[
                "quantity",
                "available_qty",
            ]
        )

    # =====================================================
    # UPDATE TRANSFER VALUE
    # =====================================================

    stock_transfer.total_cost = (
        Decimal(str(stock_transfer.quantity))
        * Decimal(str(stock_transfer.unit_cost))
    )

    # =====================================================
    # UPDATE STATUS
    # =====================================================

    stock_transfer.status = "COMPLETED"

    stock_transfer.save(
        update_fields=[
            "total_cost",
            "status",
        ]
    )

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
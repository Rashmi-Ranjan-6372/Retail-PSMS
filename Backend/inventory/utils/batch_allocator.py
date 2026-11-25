from django.db import transaction
from django.utils import timezone

from inventory.models.stock_batch_models import StockBatch

# =====================================================
# ALLOCATE BATCH - FEFO
# =====================================================


@transaction.atomic
def allocate_batch(*, product, qty, retailer, branch):

    # =====================================================
    # VALIDATE QUANTITY
    # =====================================================

    try:
        qty = int(qty)
    except (TypeError, ValueError):
        raise ValueError("Quantity must be a valid integer.")

    if qty <= 0:
        raise ValueError("Quantity must be greater than zero.")

    # =====================================================
    # VALIDATE PRODUCT OWNERSHIP
    # =====================================================

    if product.retailer_id != retailer.id:
        raise ValueError("Product does not belong to this retailer.")

    if not branch or branch.retailer_id != retailer.id:
        raise ValueError("Branch does not belong to this retailer.")

    # =====================================================
    # GET AVAILABLE BATCHES - FEFO
    # =====================================================

    batches = (
        StockBatch.objects.select_for_update()
        .filter(
            retailer=retailer,
            branch=branch,
            product=product,
            available_qty__gt=0,
            is_expired=False,
            expiry_date__gte=timezone.localdate(),
        )
        .order_by("expiry_date", "id")
    )

    # =====================================================
    # ALLOCATE STOCK
    # =====================================================

    allocated_batches = []

    remaining_qty = qty

    for batch in batches:

        if remaining_qty <= 0:
            break

        take_qty = min(batch.available_qty, remaining_qty)

        allocated_batches.append({"batch": batch, "qty": take_qty})

        remaining_qty -= take_qty

    # =====================================================
    # CHECK AVAILABLE STOCK
    # =====================================================

    if remaining_qty > 0:

        raise ValueError(
            f"Insufficient available stock for "
            f"{product.name}. "
            f"Requested: {qty}, "
            f"Available: {qty - remaining_qty}."
        )

    return allocated_batches

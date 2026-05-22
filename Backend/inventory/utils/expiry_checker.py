from datetime import timedelta

from django.utils.timezone import now

from inventory.models.stock_batch_models import (
    StockBatch
)

# =====================================================
# MARK EXPIRED BATCHES
# =====================================================

def mark_expired_batches():

    today = now().date()

    expired_batches = (
        StockBatch.objects.filter(
            expiry_date__lt=today,
            is_expired=False
        )
    )

    updated_count = 0

    for batch in expired_batches:

        batch.is_expired = True

        batch.save(
            update_fields=["is_expired"]
        )

        updated_count += 1

    return updated_count


# =====================================================
# GET EXPIRED BATCHES
# =====================================================

def get_expired_batches():

    today = now().date()

    return (
        StockBatch.objects.filter(
            expiry_date__lt=today
        )
        .select_related(
            "product",
            "supplier",
            "branch",
        )
        .order_by("expiry_date")
    )


# =====================================================
# GET NEAR EXPIRY BATCHES
# =====================================================

def get_near_expiry_batches(days=30):

    today = now().date()

    near_expiry_date = (
        today +
        timedelta(days=days)
    )

    return (
        StockBatch.objects.filter(
            expiry_date__gte=today,
            expiry_date__lte=near_expiry_date,
            is_expired=False
        )
        .select_related(
            "product",
            "supplier",
            "branch",
        )
        .order_by("expiry_date")
    )


# =====================================================
# CHECK SINGLE BATCH EXPIRY
# =====================================================

def is_batch_expired(batch):

    if not batch.expiry_date:
        return False

    return (
        batch.expiry_date <
        now().date()
    )


# =====================================================
# GET TOTAL EXPIRED STOCK VALUE
# =====================================================

def get_total_expired_stock_value():

    expired_batches = (
        StockBatch.objects.filter(
            is_expired=True
        )
    )

    total_value = 0

    for batch in expired_batches:

        total_value += (
            batch.available_qty *
            batch.purchase_price
        )

    return total_value
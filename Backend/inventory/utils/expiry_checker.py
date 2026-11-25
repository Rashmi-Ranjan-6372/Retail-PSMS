from datetime import timedelta
from decimal import Decimal

from django.db.models import F, Q, Sum, DecimalField, ExpressionWrapper
from django.utils import timezone

from inventory.models.stock_batch_models import StockBatch

# =====================================================
# MARK EXPIRED BATCHES
# =====================================================


def mark_expired_batches():

    today = timezone.localdate()

    updated_count = StockBatch.objects.filter(
        expiry_date__lt=today, is_expired=False
    ).update(is_expired=True)

    return updated_count


# =====================================================
# GET EXPIRED BATCHES
# =====================================================


def get_expired_batches(retailer=None, branch=None):

    today = timezone.localdate()

    batches = (
        StockBatch.objects.filter(expiry_date__lt=today)
        .select_related("product", "supplier", "branch", "retailer")
        .order_by("expiry_date", "id")
    )

    if retailer is not None:
        batches = batches.filter(retailer=retailer)

    if branch is not None:
        batches = batches.filter(branch=branch)

    return batches


# =====================================================
# GET NEAR EXPIRY BATCHES
# =====================================================


def get_near_expiry_batches(days=30, retailer=None, branch=None):

    if not isinstance(days, int) or isinstance(days, bool) or days < 0:
        raise ValueError("Days must be a non-negative integer.")

    today = timezone.localdate()

    near_expiry_date = today + timedelta(days=days)

    batches = (
        StockBatch.objects.filter(
            expiry_date__gte=today, expiry_date__lte=near_expiry_date, is_expired=False
        )
        .select_related("product", "supplier", "branch", "retailer")
        .order_by("expiry_date", "id")
    )

    if retailer is not None:
        batches = batches.filter(retailer=retailer)

    if branch is not None:
        batches = batches.filter(branch=branch)

    return batches


# =====================================================
# CHECK SINGLE BATCH EXPIRY
# =====================================================


def is_batch_expired(batch):

    if not batch.expiry_date:
        return False

    return batch.expiry_date < timezone.localdate()


# =====================================================
# GET TOTAL EXPIRED STOCK VALUE
# =====================================================


def get_total_expired_stock_value(retailer=None, branch=None):

    today = timezone.localdate()

    batches = StockBatch.objects.filter(Q(is_expired=True) | Q(expiry_date__lt=today))

    if retailer is not None:
        batches = batches.filter(retailer=retailer)

    if branch is not None:
        batches = batches.filter(branch=branch)

    total_value = batches.aggregate(
        total=Sum(
            ExpressionWrapper(
                F("available_qty") * F("purchase_price"),
                output_field=DecimalField(max_digits=20, decimal_places=2),
            )
        )
    )["total"]

    return total_value or Decimal("0.00")

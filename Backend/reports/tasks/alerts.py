from datetime import timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.utils.timezone import now

from inventory.models.sales_models import Sales
from inventory.models.stock_transaction_models import StockTransaction
from inventory.models.stock_batch_models import StockBatch

# =====================================================
# COMMON CONFIGURATION
# =====================================================

LOW_STOCK_LIMIT = 10


# =====================================================
# COMMON HELPER FUNCTIONS
# =====================================================


def apply_report_scope(queryset, retailer=None, branch=None):
    """
    Apply retailer and branch restrictions.

    Retailer is mandatory.
    Branch is optional for retailer-wide reports.
    Platform Owner global reports must use a separate
    explicitly authorized reporting path.
    """

    if retailer is None:
        raise ValidationError("Retailer scope is required.")

    if branch is not None and branch.retailer_id != retailer.id:
        raise ValidationError("The selected branch does not belong to this retailer.")

    queryset = queryset.filter(
        retailer_id=retailer.id,
    )

    if branch is not None:
        queryset = queryset.filter(
            branch_id=branch.id,
        )

    return queryset


def get_decimal_sum(queryset, field_name):
    """
    Calculate a decimal sum without forcing money precision
    onto quantity fields.
    """

    result = queryset.aggregate(
        total=Sum(field_name),
    )["total"]

    return result if result is not None else Decimal("0.00")


def validate_non_negative_number(value, field_name):
    """
    Validate that a numeric input is not negative.
    """

    try:
        value = Decimal(str(value))
    except (TypeError, ValueError, ArithmeticError):
        raise ValidationError(f"{field_name} must be a valid number.")

    if not value.is_finite() or value < 0:
        raise ValidationError(f"{field_name} cannot be negative.")

    return value


# =====================================================
# DAILY REPORT
# =====================================================


def generate_daily_report(retailer=None, branch=None):
    """
    Generate today's sales and purchase summary.
    """

    today = now().date()

    sales_queryset = apply_report_scope(
        Sales.objects.filter(
            created_at__date=today,
        ),
        retailer=retailer,
        branch=branch,
    )

    purchase_queryset = apply_report_scope(
        StockTransaction.objects.filter(
            transaction_type="PURCHASE",
            created_at__date=today,
        ),
        retailer=retailer,
        branch=branch,
    )

    sales_total = get_decimal_sum(
        sales_queryset,
        "net_amount",
    )

    purchase_total = get_decimal_sum(
        purchase_queryset,
        "total_amount",
    )

    return {
        "date": today,
        "sales_total": sales_total,
        "purchase_total": purchase_total,
        "profit": None,
    }


# =====================================================
# MONTHLY REPORT
# =====================================================


def generate_monthly_report(retailer=None, branch=None):
    """
    Generate the current month's sales and purchase summary.
    """

    today = now()

    sales_queryset = apply_report_scope(
        Sales.objects.filter(
            created_at__year=today.year,
            created_at__month=today.month,
        ),
        retailer=retailer,
        branch=branch,
    )

    purchase_queryset = apply_report_scope(
        StockTransaction.objects.filter(
            transaction_type="PURCHASE",
            created_at__year=today.year,
            created_at__month=today.month,
        ),
        retailer=retailer,
        branch=branch,
    )

    sales_total = get_decimal_sum(
        sales_queryset,
        "net_amount",
    )

    purchase_total = get_decimal_sum(
        purchase_queryset,
        "total_amount",
    )

    return {
        "month": today.month,
        "year": today.year,
        "sales_total": sales_total,
        "purchase_total": purchase_total,
        "profit": None,
    }


# =====================================================
# EXPIRY ALERTS
# =====================================================


def get_expiry_alerts(
    days=30,
    retailer=None,
    branch=None,
):
    """
    Return stock batches expiring within the next N days.

    Already expired batches are excluded.
    """

    days = validate_non_negative_number(
        days,
        "Days",
    )

    if days != days.to_integral_value():
        raise ValidationError("Days must be a whole number.")

    expiry_days = int(days)

    today = now().date()

    expiry_date = today + timedelta(
        days=expiry_days,
    )

    queryset = StockBatch.objects.filter(
        expiry_date__gte=today,
        expiry_date__lte=expiry_date,
        is_expired=False,
        available_qty__gt=0,
    )

    batches = (
        apply_report_scope(
            queryset,
            retailer=retailer,
            branch=branch,
        )
        .select_related(
            "product",
            "branch",
        )
        .order_by(
            "expiry_date",
        )
    )

    return [
        {
            "product": batch.product.name,
            "batch_no": batch.batch_no,
            "branch": (batch.branch.name if batch.branch_id else None),
            "expiry_date": batch.expiry_date,
            "available_qty": batch.available_qty,
            "days_remaining": (batch.expiry_date - today).days,
        }
        for batch in batches
    ]


# =====================================================
# LOW STOCK ALERTS
# =====================================================


def get_low_stock_alerts(
    retailer=None,
    branch=None,
    threshold=LOW_STOCK_LIMIT,
):
    """
    Return stock batches with available quantity
    greater than zero and less than or equal to threshold.
    """

    threshold = validate_non_negative_number(
        threshold,
        "Stock threshold",
    )

    queryset = StockBatch.objects.filter(
        available_qty__gt=0,
        available_qty__lte=threshold,
    )

    batches = (
        apply_report_scope(
            queryset,
            retailer=retailer,
            branch=branch,
        )
        .select_related(
            "product",
            "branch",
        )
        .order_by(
            "available_qty",
        )
    )

    return [
        {
            "product": batch.product.name,
            "batch_no": batch.batch_no,
            "branch": (batch.branch.name if batch.branch_id else None),
            "available_qty": batch.available_qty,
            "threshold": threshold,
        }
        for batch in batches
    ]

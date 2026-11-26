from datetime import timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db.models import Sum, DecimalField
from django.db.models.functions import Coalesce
from django.utils.timezone import now

from inventory.models.sales_models import Sales
from inventory.models.stock_transaction_models import StockTransaction
from inventory.models.stock_batch_models import StockBatch

LOW_STOCK_LIMIT = 10

MONEY_FIELD = DecimalField(max_digits=15, decimal_places=2)


def apply_report_scope(queryset, retailer=None, branch=None):
    if retailer is None and branch is None:
        raise ValidationError("Retailer or branch scope is required.")

    if retailer is not None:
        queryset = queryset.filter(retailer=retailer)

    if branch is not None:
        queryset = queryset.filter(branch=branch)

    return queryset


def get_decimal_sum(queryset, field_name):
    return queryset.aggregate(
        total=Coalesce(Sum(field_name), Decimal("0.00"), output_field=MONEY_FIELD)
    )["total"]


def generate_daily_report(retailer=None, branch=None):
    today = now().date()

    sales_queryset = apply_report_scope(
        Sales.objects.filter(created_at__date=today), retailer, branch
    )

    purchase_queryset = apply_report_scope(
        StockTransaction.objects.filter(
            transaction_type="PURCHASE", created_at__date=today
        ),
        retailer,
        branch,
    )

    sales_total = get_decimal_sum(sales_queryset, "net_amount")

    purchase_total = get_decimal_sum(purchase_queryset, "total_amount")

    return {
        "date": today,
        "sales_total": sales_total,
        "purchase_total": purchase_total,
        "profit": None,
    }


def generate_monthly_report(retailer=None, branch=None):
    today = now()

    sales_queryset = apply_report_scope(
        Sales.objects.filter(
            created_at__year=today.year, created_at__month=today.month
        ),
        retailer,
        branch,
    )

    purchase_queryset = apply_report_scope(
        StockTransaction.objects.filter(
            transaction_type="PURCHASE",
            created_at__year=today.year,
            created_at__month=today.month,
        ),
        retailer,
        branch,
    )

    sales_total = get_decimal_sum(sales_queryset, "net_amount")

    purchase_total = get_decimal_sum(purchase_queryset, "total_amount")

    return {
        "month": today.month,
        "year": today.year,
        "sales_total": sales_total,
        "purchase_total": purchase_total,
        "profit": None,
    }


def get_expiry_alerts(days=30, retailer=None, branch=None):
    if days < 0:
        raise ValidationError("Days cannot be negative.")

    expiry_date = now().date() + timedelta(days=days)

    queryset = StockBatch.objects.filter(
        expiry_date__lte=expiry_date,
        expiry_date__gte=now().date(),
        is_expired=False,
        available_qty__gt=0,
    )

    batches = (
        apply_report_scope(queryset, retailer, branch)
        .select_related("product")
        .order_by("expiry_date")
    )

    return [
        {
            "product": batch.product.name,
            "batch_no": batch.batch_no,
            "expiry_date": batch.expiry_date,
            "available_qty": batch.available_qty,
        }
        for batch in batches
    ]


def get_low_stock_alerts(retailer=None, branch=None, threshold=LOW_STOCK_LIMIT):
    if threshold < 0:
        raise ValidationError("Stock threshold cannot be negative.")

    queryset = StockBatch.objects.filter(
        available_qty__lte=threshold, available_qty__gt=0
    )

    batches = (
        apply_report_scope(queryset, retailer, branch)
        .select_related("product")
        .order_by("available_qty")
    )

    return [
        {
            "product": batch.product.name,
            "batch_no": batch.batch_no,
            "available_qty": batch.available_qty,
        }
        for batch in batches
    ]

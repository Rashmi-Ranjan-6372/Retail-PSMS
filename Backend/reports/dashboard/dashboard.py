from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db.models import Sum, Count, DecimalField
from django.db.models.functions import Coalesce, TruncMonth
from django.utils.timezone import now

from inventory.models.sales_models import Sales
from inventory.models.payment_models import Payment
from inventory.models.receipt_models import Receipt
from inventory.models.stock_batch_models import StockBatch

# =========================
# COMMON DASHBOARD HELPERS
# =========================

MONEY_FIELD = DecimalField(max_digits=15, decimal_places=2)


def apply_dashboard_scope(queryset, retailer=None, branch=None):
    """
    Apply retailer and branch ownership filters.

    A global dashboard must be explicitly handled separately.
    """

    if retailer is None and branch is None:
        raise ValidationError(
            "Retailer or branch scope is required for dashboard data."
        )

    if retailer is not None:
        queryset = queryset.filter(retailer=retailer)

    if branch is not None:
        queryset = queryset.filter(branch=branch)

    return queryset


def decimal_sum(queryset, field_name):
    return queryset.aggregate(
        total=Coalesce(
            Sum(field_name),
            Decimal("0.00"),
            output_field=MONEY_FIELD,
        )
    )["total"]


# =========================
# ANALYTICS DASHBOARD
# =========================


class AnalyticsDashboardService:

    @staticmethod
    def monthly_sales(retailer=None, branch=None):

        queryset = apply_dashboard_scope(
            Sales.objects.all(),
            retailer=retailer,
            branch=branch,
        )

        return (
            queryset.annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(
                total_sales=Coalesce(
                    Sum("net_amount"),
                    Decimal("0.00"),
                    output_field=MONEY_FIELD,
                )
            )
            .order_by("month")
        )


# =========================
# FINANCE DASHBOARD
# =========================


class FinanceDashboardService:

    @staticmethod
    def get_dashboard(retailer=None, branch=None):

        payment_queryset = apply_dashboard_scope(
            Payment.objects.all(),
            retailer=retailer,
            branch=branch,
        )

        receipt_queryset = apply_dashboard_scope(
            Receipt.objects.all(),
            retailer=retailer,
            branch=branch,
        )

        return {
            "total_payment": decimal_sum(
                payment_queryset,
                "paid_amount",
            ),
            "total_receipt": decimal_sum(
                receipt_queryset,
                "paid_amount",
            ),
            "pending_payment": decimal_sum(
                payment_queryset.filter(status="PENDING"),
                "due_amount",
            ),
            "pending_receipt": decimal_sum(
                receipt_queryset.filter(status="PENDING"),
                "due_amount",
            ),
        }


# =========================
# SALES DASHBOARD
# =========================


class SalesDashboardService:

    @staticmethod
    def get_dashboard(retailer=None, branch=None):

        queryset = apply_dashboard_scope(
            Sales.objects.all(),
            retailer=retailer,
            branch=branch,
        )

        return {
            "total_sales": decimal_sum(
                queryset,
                "net_amount",
            ),
            "total_invoices": queryset.aggregate(total=Count("id"))["total"],
            "paid_sales": queryset.filter(payment_status="PAID").count(),
            "unpaid_sales": queryset.filter(payment_status="UNPAID").count(),
        }


# =========================
# STOCK DASHBOARD
# =========================


class StockDashboardService:

    LOW_STOCK_THRESHOLD = 10

    @staticmethod
    def get_dashboard(retailer=None, branch=None):

        queryset = apply_dashboard_scope(
            StockBatch.objects.all(),
            retailer=retailer,
            branch=branch,
        )

        today = now().date()

        return {
            "total_stock_qty": queryset.aggregate(
                total=Coalesce(
                    Sum("available_qty"),
                    Decimal("0.00"),
                    output_field=MONEY_FIELD,
                )
            )["total"],
            "expired_products": queryset.filter(expiry_date__lt=today).count(),
            "low_stock_products": queryset.filter(
                available_qty__lte=StockDashboardService.LOW_STOCK_THRESHOLD,
                available_qty__gt=0,
                expiry_date__gte=today,
            ).count(),
        }


# =========================
# SUMMARY DASHBOARD
# =========================


class SummaryDashboardService:

    @staticmethod
    def get_dashboard(retailer=None, branch=None):

        if retailer is None and branch is None:
            raise ValidationError(
                "Retailer or branch scope is required for dashboard data."
            )

        sales_data = SalesDashboardService.get_dashboard(
            retailer=retailer,
            branch=branch,
        )

        stock_data = StockDashboardService.get_dashboard(
            retailer=retailer,
            branch=branch,
        )

        finance_data = FinanceDashboardService.get_dashboard(
            retailer=retailer,
            branch=branch,
        )

        return {
            "sales": sales_data,
            "stock": stock_data,
            "finance": finance_data,
        }

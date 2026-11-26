import django_filters

from inventory.models.sales_models import Sales
from inventory.models.payment_models import Payment
from inventory.models.stock_transaction_models import StockTransaction
from inventory.models.stock_batch_models import StockBatch

# =========================
# COMMON DATE FILTERS
# =========================


class DateRangeFilterMixin:

    start_date = django_filters.DateFilter(
        field_name="created_at__date",
        lookup_expr="gte",
    )

    end_date = django_filters.DateFilter(
        field_name="created_at__date",
        lookup_expr="lte",
    )


# =========================
# DASHBOARD FILTER
# =========================


class DashboardFilter(DateRangeFilterMixin, django_filters.FilterSet):

    branch = django_filters.NumberFilter(
        field_name="branch_id",
    )

    class Meta:
        model = Sales
        fields = [
            "branch",
        ]


# =========================
# CUSTOMER LEDGER FILTER
# =========================


class CustomerLedgerFilter(DateRangeFilterMixin, django_filters.FilterSet):

    customer = django_filters.NumberFilter(
        field_name="customer_id",
    )

    class Meta:
        model = Sales
        fields = [
            "customer",
        ]


# =========================
# SUPPLIER LEDGER FILTER
# =========================


class SupplierLedgerFilter(DateRangeFilterMixin, django_filters.FilterSet):

    supplier = django_filters.NumberFilter(
        field_name="supplier_id",
    )

    class Meta:
        model = Payment
        fields = [
            "supplier",
        ]


# =========================
# PURCHASE REPORT FILTER
# =========================


class PurchaseReportFilter(DateRangeFilterMixin, django_filters.FilterSet):

    supplier = django_filters.NumberFilter(
        field_name="supplier_id",
    )

    branch = django_filters.NumberFilter(
        field_name="branch_id",
    )

    transaction_type = django_filters.CharFilter(
        field_name="transaction_type",
        lookup_expr="exact",
    )

    class Meta:
        model = StockTransaction
        fields = [
            "supplier",
            "branch",
            "transaction_type",
        ]


# =========================
# SALES REPORT FILTER
# =========================


class SalesReportFilter(DateRangeFilterMixin, django_filters.FilterSet):

    customer = django_filters.NumberFilter(
        field_name="customer_id",
    )

    payment_status = django_filters.CharFilter(
        field_name="payment_status",
        lookup_expr="exact",
    )

    branch = django_filters.NumberFilter(
        field_name="branch_id",
    )

    class Meta:
        model = Sales
        fields = [
            "customer",
            "payment_status",
            "branch",
        ]


# =========================
# STOCK REPORT FILTER
# =========================


class StockReportFilter(django_filters.FilterSet):

    product = django_filters.NumberFilter(
        field_name="product_id",
    )

    supplier = django_filters.NumberFilter(
        field_name="supplier_id",
    )

    branch = django_filters.NumberFilter(
        field_name="branch_id",
    )

    is_expired = django_filters.BooleanFilter(
        field_name="is_expired",
    )

    class Meta:
        model = StockBatch
        fields = [
            "product",
            "supplier",
            "branch",
            "is_expired",
        ]

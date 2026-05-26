import django_filters
from inventory.models.stock_transaction_models import StockTransaction


class PurchaseReportFilter(django_filters.FilterSet):

    start_date = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="date__gte"
    )

    end_date = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="date__lte"
    )

    supplier = django_filters.NumberFilter(
        field_name="supplier_id"
    )

    branch = django_filters.NumberFilter(
        field_name="branch_id"
    )

    class Meta:
        model = StockTransaction

        fields = [
            "supplier",
            "branch",
            "transaction_type"
        ]
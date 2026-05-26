import django_filters
from inventory.models.stock_batch_models import StockBatch


class StockReportFilter(django_filters.FilterSet):

    product = django_filters.NumberFilter(
        field_name="product_id"
    )

    supplier = django_filters.NumberFilter(
        field_name="supplier_id"
    )

    branch = django_filters.NumberFilter(
        field_name="branch_id"
    )

    is_expired = django_filters.BooleanFilter(
        field_name="is_expired"
    )

    class Meta:
        model = StockBatch

        fields = [
            "product",
            "supplier",
            "branch",
            "is_expired"
        ]
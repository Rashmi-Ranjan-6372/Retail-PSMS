import django_filters
from inventory.models.sales_models import Sales
from inventory.models.payment_models import Payment


class CustomerLedgerFilter(django_filters.FilterSet):

    customer = django_filters.NumberFilter(
        field_name="customer_id"
    )

    start_date = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="date__gte"
    )

    end_date = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="date__lte"
    )

    class Meta:
        model = Sales

        fields = [
            "customer"
        ]


class SupplierLedgerFilter(django_filters.FilterSet):

    supplier = django_filters.NumberFilter(
        field_name="supplier_id"
    )

    start_date = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="date__gte"
    )

    end_date = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="date__lte"
    )

    class Meta:
        model = Payment

        fields = [
            "supplier"
        ]
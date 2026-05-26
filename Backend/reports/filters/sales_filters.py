import django_filters
from inventory.models.sales_models import Sales


class SalesReportFilter(django_filters.FilterSet):

    start_date = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="date__gte"
    )

    end_date = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="date__lte"
    )

    customer = django_filters.NumberFilter(
        field_name="customer_id"
    )

    payment_status = django_filters.CharFilter(
        field_name="payment_status"
    )

    branch = django_filters.NumberFilter(
        field_name="branch_id"
    )

    class Meta:
        model = Sales

        fields = [
            "customer",
            "payment_status",
            "branch"
        ]
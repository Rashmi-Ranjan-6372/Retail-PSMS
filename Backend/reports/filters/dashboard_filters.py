import django_filters
from inventory.models.sales_models import Sales


class DashboardFilter(django_filters.FilterSet):

    branch = django_filters.NumberFilter(
        field_name="branch_id"
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
            "branch"
        ]
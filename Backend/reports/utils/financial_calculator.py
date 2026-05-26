from django.db.models import Sum
from django.db.models.functions import Coalesce


def calculate_sales_total(queryset):

    return queryset.aggregate(
        total=Coalesce(Sum("net_amount"), 0)
    )["total"]


def calculate_purchase_total(queryset):

    return queryset.aggregate(
        total=Coalesce(Sum("total_amount"), 0)
    )["total"]


def calculate_profit(sales, purchase):

    return sales - purchase
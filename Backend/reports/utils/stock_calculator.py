from django.db.models import Sum
from django.db.models.functions import Coalesce


def total_stock(queryset):

    return queryset.aggregate(
        total=Coalesce(Sum("available_qty"), 0)
    )["total"]


def low_stock(queryset, limit=10):

    return queryset.filter(
        available_qty__lte=limit
    )


def expired_stock(queryset):

    return queryset.filter(
        is_expired=True
    )
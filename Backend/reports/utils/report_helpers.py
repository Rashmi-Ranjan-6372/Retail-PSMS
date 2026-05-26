from django.db.models import Sum
from django.db.models.functions import Coalesce


def calculate_total(queryset, field):

    return queryset.aggregate(
        total=Coalesce(Sum(field), 0)
    )["total"]


def format_currency(amount):

    return round(float(amount), 2)


def get_percentage(value, total):

    if total == 0:
        return 0

    return round((value / total) * 100, 2)
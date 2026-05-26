from django.db.models import Sum
from django.db.models.functions import Coalesce


def calculate_supplier_balance(queryset):

    total = queryset.aggregate(
        total=Coalesce(Sum("due_amount"), 0)
    )["total"]

    return total


def calculate_customer_balance(queryset):

    total = queryset.aggregate(
        total=Coalesce(Sum("due_amount"), 0)
    )["total"]

    return total
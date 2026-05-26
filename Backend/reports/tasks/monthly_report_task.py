from django.utils.timezone import now
from inventory.models.sales_models import Sales
from inventory.models.purchase_models import Purchase
from django.db.models import Sum
from django.db.models.functions import Coalesce


def generate_monthly_report():

    today = now()

    sales_total = Sales.objects.filter(
        created_at__year=today.year,
        created_at__month=today.month
    ).aggregate(
        total=Coalesce(Sum("net_amount"), 0)
    )["total"]

    purchase_total = Purchase.objects.filter(
        created_at__year=today.year,
        created_at__month=today.month
    ).aggregate(
        total=Coalesce(Sum("net_amount"), 0)
    )["total"]

    return {
        "month": today.month,
        "year": today.year,
        "sales_total": sales_total,
        "purchase_total": purchase_total,
        "profit": sales_total - purchase_total
    }
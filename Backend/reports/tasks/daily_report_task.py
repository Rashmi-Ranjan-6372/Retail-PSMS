from django.utils.timezone import now
from inventory.models.sales_models import Sales
from inventory.models.purchase_models import Purchase
from django.db.models import Sum
from django.db.models.functions import Coalesce


def generate_daily_report():

    today = now().date()

    sales_total = Sales.objects.filter(
        created_at__date=today
    ).aggregate(
        total=Coalesce(Sum("net_amount"), 0)
    )["total"]

    purchase_total = Purchase.objects.filter(
        created_at__date=today
    ).aggregate(
        total=Coalesce(Sum("net_amount"), 0)
    )["total"]

    return {
        "date": today,
        "sales_total": sales_total,
        "purchase_total": purchase_total,
        "profit": sales_total - purchase_total
    }
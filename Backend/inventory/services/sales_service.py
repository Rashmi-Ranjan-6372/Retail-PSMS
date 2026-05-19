from django.db.models import Sum
from inventory.models.sales_item_models import SalesItem


class SalesService:

    @staticmethod
    def calculate_sales_total(sales):

        total = (
            SalesItem.objects.filter(
                sales=sales
            ).aggregate(
                total=Sum("amount")
            )["total"] or 0
        )

        sales.total_amount = total
        sales.save()

        return sales
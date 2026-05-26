from inventory.models.sales_item_models import SalesItem
from django.db.models import Sum
from django.db.models.functions import Coalesce


class GSTReportService:

    @staticmethod
    def get_report():

        return SalesItem.objects.aggregate(
            total_tax=Coalesce(Sum("tax_amount"), 0)
        )
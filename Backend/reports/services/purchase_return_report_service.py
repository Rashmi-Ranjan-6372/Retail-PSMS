from inventory.models.purchase_return_models import PurchaseReturn
from django.db.models import Sum
from django.db.models.functions import Coalesce


class PurchaseReturnReportService:

    @staticmethod
    def get_report():

        queryset = PurchaseReturn.objects.all()

        summary = queryset.aggregate(
            total_returns=Coalesce(Sum("total_amount"), 0)
        )

        return {
            "summary": summary,
            "data": queryset
        }
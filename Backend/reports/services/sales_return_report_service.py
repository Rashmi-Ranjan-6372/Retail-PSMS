from inventory.models.sales_return_models import SalesReturn
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce


class SalesReturnReportService:

    @staticmethod
    def get_report():

        queryset = SalesReturn.objects.all()

        summary = queryset.aggregate(
            total_returns=Coalesce(Sum("total_amount"), 0),
            refund_amount=Coalesce(Sum("refund_amount"), 0),
            return_count=Count("id")
        )

        return {
            "summary": summary,
            "data": queryset
        }
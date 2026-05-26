from inventory.models.receipt_models import Receipt
from django.db.models import Sum
from django.db.models.functions import Coalesce


class ReceiptReportService:

    @staticmethod
    def get_report():

        queryset = Receipt.objects.all()

        summary = queryset.aggregate(
            total_receipt=Coalesce(Sum("paid_amount"), 0)
        )

        return {
            "summary": summary,
            "data": queryset
        }
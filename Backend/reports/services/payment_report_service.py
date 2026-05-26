from inventory.models.payment_models import Payment
from django.db.models import Sum
from django.db.models.functions import Coalesce


class PaymentReportService:

    @staticmethod
    def get_report():

        queryset = Payment.objects.all()

        summary = queryset.aggregate(
            total_payment=Coalesce(Sum("paid_amount"), 0)
        )

        return {
            "summary": summary,
            "data": queryset
        }
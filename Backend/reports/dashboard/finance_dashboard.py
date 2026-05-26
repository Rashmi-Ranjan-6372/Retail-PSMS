from inventory.models.payment_models import Payment
from inventory.models.receipt_models import Receipt
from django.db.models import Sum
from django.db.models.functions import Coalesce


class FinanceDashboardService:

    @staticmethod
    def get_dashboard(retailer=None, branch=None):

        payment_queryset = Payment.objects.all()
        receipt_queryset = Receipt.objects.all()

        if retailer:
            payment_queryset = payment_queryset.filter(
                retailer=retailer
            )

            receipt_queryset = receipt_queryset.filter(
                retailer=retailer
            )

        if branch:
            payment_queryset = payment_queryset.filter(
                branch=branch
            )

            receipt_queryset = receipt_queryset.filter(
                branch=branch
            )

        return {

            "total_payment": payment_queryset.aggregate(
                total=Coalesce(Sum("paid_amount"), 0)
            )["total"],

            "total_receipt": receipt_queryset.aggregate(
                total=Coalesce(Sum("paid_amount"), 0)
            )["total"],

            "pending_payment": payment_queryset.filter(
                status="PENDING"
            ).aggregate(
                total=Coalesce(Sum("due_amount"), 0)
            )["total"],

            "pending_receipt": receipt_queryset.filter(
                status="PENDING"
            ).aggregate(
                total=Coalesce(Sum("due_amount"), 0)
            )["total"],
        }
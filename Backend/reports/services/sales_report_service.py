from inventory.models.sales_models import Sales
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce


class SalesReportService:

    @staticmethod
    def get_sales_report(filters=None):

        queryset = Sales.objects.all()

        if filters:

            if filters.get("retailer"):
                queryset = queryset.filter(
                    retailer=filters["retailer"]
                )

            if filters.get("branch"):
                queryset = queryset.filter(
                    branch=filters["branch"]
                )

            if filters.get("from_date"):
                queryset = queryset.filter(
                    created_at__date__gte=filters["from_date"]
                )

            if filters.get("to_date"):
                queryset = queryset.filter(
                    created_at__date__lte=filters["to_date"]
                )

        summary = queryset.aggregate(
            total_sales=Coalesce(Sum("net_amount"), 0),
            total_paid=Coalesce(Sum("paid_amount"), 0),
            total_due=Coalesce(Sum("due_amount"), 0),
            invoice_count=Count("id")
        )

        return {
            "summary": summary,
            "data": queryset
        }
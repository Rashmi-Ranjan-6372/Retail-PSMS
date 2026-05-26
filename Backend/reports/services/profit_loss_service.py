from inventory.models.sales_models import Sales
from inventory.models.stock_transaction_models import StockTransaction

from django.db.models import Sum
from django.db.models.functions import Coalesce


class ProfitLossService:

    @staticmethod
    def get_report(retailer=None):

        # =========================
        # SALES TOTAL
        # =========================

        sales_queryset = Sales.objects.all()

        if retailer:
            sales_queryset = sales_queryset.filter(
                retailer=retailer
            )

        sales_total = sales_queryset.aggregate(
            total=Coalesce(
                Sum("net_amount"),
                0
            )
        )["total"]

        # =========================
        # PURCHASE TOTAL
        # =========================

        purchase_queryset = (
            StockTransaction.objects.filter(
                transaction_type="PURCHASE"
            )
        )

        if retailer:
            purchase_queryset = purchase_queryset.filter(
                retailer=retailer
            )

        purchase_total = purchase_queryset.aggregate(
            total=Coalesce(
                Sum("total_amount"),
                0
            )
        )["total"]

        # =========================
        # PROFIT
        # =========================

        profit = (
            sales_total -
            purchase_total
        )

        # =========================
        # BRANCH WISE PROFIT LOSS
        # =========================

        branch_wise = []

        branches = sales_queryset.values(
            "branch__id",
            "branch__name"
        ).distinct()

        for branch in branches:

            branch_id = branch["branch__id"]

            branch_sales = (
                sales_queryset.filter(
                    branch_id=branch_id
                ).aggregate(
                    total=Coalesce(
                        Sum("net_amount"),
                        0
                    )
                )["total"]
            )

            branch_purchase = (
                purchase_queryset.filter(
                    branch_id=branch_id
                ).aggregate(
                    total=Coalesce(
                        Sum("total_amount"),
                        0
                    )
                )["total"]
            )

            branch_profit = (
                branch_sales -
                branch_purchase
            )

            branch_wise.append({
                "branch_id": branch_id,
                "branch_name": branch["branch__name"],
                "sales": branch_sales,
                "purchase": branch_purchase,
                "profit": branch_profit
            })

        return {
            "overall": {
                "sales": sales_total,
                "purchase": purchase_total,
                "profit": profit
            },
            "branch_wise": branch_wise
        }
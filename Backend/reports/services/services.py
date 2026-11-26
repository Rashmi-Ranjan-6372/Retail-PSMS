from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db.models import Sum, Count, DecimalField
from django.db.models.functions import Coalesce
from django.utils.timezone import now

from inventory.models.sales_models import Sales
from inventory.models.sales_item_models import SalesItem
from inventory.models.sales_return_models import SalesReturn

from inventory.models.stock_transaction_models import StockTransaction
from inventory.models.stock_transaction_item_models import StockTransactionItem
from inventory.models.stock_batch_models import StockBatch
from inventory.models.stock_adjustment_models import StockAdjustment
from inventory.models.stock_transfer_models import StockTransfer

from inventory.models.payment_models import Payment
from inventory.models.receipt_models import Receipt
from inventory.models.purchase_return_models import PurchaseReturn

# =========================
# COMMON CONFIGURATION
# =========================

MONEY_FIELD = DecimalField(
    max_digits=15,
    decimal_places=2,
)

LOW_STOCK_THRESHOLD = 10


# =========================
# COMMON HELPER FUNCTIONS
# =========================


def apply_report_scope(queryset, retailer=None, branch=None):
    """
    Apply retailer and branch filters to report querysets.

    At least one scope must be provided.
    Platform Owner global reports should use a separate
    explicitly authorized path.
    """

    if retailer is None and branch is None:
        raise ValidationError("Retailer or branch scope is required.")

    if retailer is not None:
        queryset = queryset.filter(retailer=retailer)

    if branch is not None:
        queryset = queryset.filter(branch=branch)

    return queryset


def get_decimal_sum(queryset, field_name):
    """
    Return a decimal sum with a zero default.
    """

    return queryset.aggregate(
        total=Coalesce(
            Sum(field_name),
            Decimal("0.00"),
            output_field=MONEY_FIELD,
        )
    )["total"]


# =========================
# ANALYTICS SERVICE
# =========================


class AnalyticsService:

    @staticmethod
    def get_analytics(retailer=None, branch=None):

        sales_queryset = apply_report_scope(
            Sales.objects.all(),
            retailer=retailer,
            branch=branch,
        )

        purchase_queryset = apply_report_scope(
            StockTransaction.objects.filter(transaction_type="PURCHASE"),
            retailer=retailer,
            branch=branch,
        )

        total_sales = get_decimal_sum(
            sales_queryset,
            "net_amount",
        )

        total_purchase = get_decimal_sum(
            purchase_queryset,
            "total_amount",
        )

        total_customers = (
            sales_queryset.filter(customer__isnull=False)
            .values("customer_id")
            .distinct()
            .count()
        )

        total_suppliers = (
            purchase_queryset.filter(supplier__isnull=False)
            .values("supplier_id")
            .distinct()
            .count()
        )

        return {
            "total_sales": total_sales,
            "total_purchase": total_purchase,
            "total_profit": None,
            "total_customers": total_customers,
            "total_suppliers": total_suppliers,
        }


# =========================
# CUSTOMER LEDGER SERVICE
# =========================


class CustomerLedgerService:

    @staticmethod
    def get_customer_ledger(
        customer_id,
        retailer=None,
        branch=None,
    ):

        queryset = apply_report_scope(
            Sales.objects.all(),
            retailer=retailer,
            branch=branch,
        )

        return queryset.filter(customer_id=customer_id).order_by("-created_at")


# =========================
# DASHBOARD SERVICE
# =========================


class DashboardService:

    @staticmethod
    def get_dashboard(retailer=None, branch=None):

        sales_queryset = apply_report_scope(
            Sales.objects.all(),
            retailer=retailer,
            branch=branch,
        )

        stock_queryset = apply_report_scope(
            StockBatch.objects.all(),
            retailer=retailer,
            branch=branch,
        )

        return {
            "total_sales": get_decimal_sum(
                sales_queryset,
                "net_amount",
            ),
            "invoice_count": sales_queryset.aggregate(count=Count("id"))["count"],
            "total_stock": get_decimal_sum(
                stock_queryset,
                "available_qty",
            ),
        }


# =========================
# EXPIRY REPORT SERVICE
# =========================


class ExpiryReportService:

    @staticmethod
    def get_report(retailer=None, branch=None):

        queryset = apply_report_scope(
            StockBatch.objects.all(),
            retailer=retailer,
            branch=branch,
        )

        return queryset.filter(expiry_date__lt=now().date()).order_by("expiry_date")


# =========================
# GST REPORT SERVICE
# =========================


class GSTReportService:

    @staticmethod
    def get_report(retailer=None, branch=None):

        queryset = apply_report_scope(
            SalesItem.objects.all(),
            retailer=retailer,
            branch=branch,
        )

        return {
            "total_tax": get_decimal_sum(
                queryset,
                "tax_amount",
            )
        }


# =========================
# TAX REPORT SERVICE
# =========================


class TaxReportService(GSTReportService):
    """
    Reuses GST report calculation.
    """


# =========================
# LOW STOCK REPORT SERVICE
# =========================


class LowStockReportService:

    @staticmethod
    def get_report(
        retailer=None,
        branch=None,
        threshold=LOW_STOCK_THRESHOLD,
    ):

        if threshold < 0:
            raise ValidationError("Stock threshold cannot be negative.")

        queryset = apply_report_scope(
            StockBatch.objects.all(),
            retailer=retailer,
            branch=branch,
        )

        return queryset.filter(
            available_qty__gt=0,
            available_qty__lte=threshold,
        ).order_by("available_qty")


# =========================
# PAYMENT REPORT SERVICE
# =========================


class PaymentReportService:

    @staticmethod
    def get_report(retailer=None, branch=None):

        queryset = apply_report_scope(
            Payment.objects.all(),
            retailer=retailer,
            branch=branch,
        )

        summary = {
            "total_payment": get_decimal_sum(
                queryset,
                "paid_amount",
            ),
            "payment_count": queryset.count(),
        }

        return {
            "summary": summary,
            "data": queryset.order_by("-created_at"),
        }


# =========================
# PRODUCT LEDGER SERVICE
# =========================


class ProductLedgerService:

    @staticmethod
    def get_product_ledger(
        product_id,
        retailer=None,
        branch=None,
    ):

        queryset = apply_report_scope(
            StockTransactionItem.objects.all(),
            retailer=retailer,
            branch=branch,
        )

        return queryset.filter(product_id=product_id).order_by("created_at")


# =========================
# PROFIT & LOSS SERVICE
# =========================


class ProfitLossService:

    @staticmethod
    def get_report(retailer=None, branch=None):

        sales_queryset = apply_report_scope(
            Sales.objects.all(),
            retailer=retailer,
            branch=branch,
        )

        purchase_queryset = apply_report_scope(
            StockTransaction.objects.filter(transaction_type="PURCHASE"),
            retailer=retailer,
            branch=branch,
        )

        sales_total = get_decimal_sum(
            sales_queryset,
            "net_amount",
        )

        purchase_total = get_decimal_sum(
            purchase_queryset,
            "total_amount",
        )

        return {
            "overall": {
                "sales": sales_total,
                "purchase": purchase_total,
                "profit": None,
            },
            "branch_wise": [],
            "message": (
                "Profit calculation requires the cost of goods sold "
                "(COGS), sales returns, and applicable adjustments. "
                "Sales minus purchases is not actual profit."
            ),
        }


# =========================
# PURCHASE REPORT SERVICE
# =========================


class PurchaseReportService:

    @staticmethod
    def get_report(retailer=None, branch=None):

        queryset = apply_report_scope(
            StockTransaction.objects.filter(transaction_type="PURCHASE"),
            retailer=retailer,
            branch=branch,
        )

        summary = {
            "total_purchase": get_decimal_sum(
                queryset,
                "total_amount",
            ),
            "purchase_count": queryset.count(),
        }

        return {
            "summary": summary,
            "data": queryset.order_by("-created_at"),
        }


# =========================
# PURCHASE RETURN REPORT SERVICE
# =========================


class PurchaseReturnReportService:

    @staticmethod
    def get_report(retailer=None, branch=None):

        queryset = apply_report_scope(
            PurchaseReturn.objects.all(),
            retailer=retailer,
            branch=branch,
        )

        summary = {
            "total_returns": get_decimal_sum(
                queryset,
                "total_amount",
            ),
            "return_count": queryset.count(),
        }

        return {
            "summary": summary,
            "data": queryset.order_by("-created_at"),
        }


# =========================
# RECEIPT REPORT SERVICE
# =========================


class ReceiptReportService:

    @staticmethod
    def get_report(retailer=None, branch=None):

        queryset = apply_report_scope(
            Receipt.objects.all(),
            retailer=retailer,
            branch=branch,
        )

        summary = {
            "total_receipt": get_decimal_sum(
                queryset,
                "paid_amount",
            ),
            "receipt_count": queryset.count(),
        }

        return {
            "summary": summary,
            "data": queryset.order_by("-created_at"),
        }


# =========================
# SALES REPORT SERVICE
# =========================


class SalesReportService:

    @staticmethod
    def get_sales_report(
        filters=None,
        retailer=None,
        branch=None,
    ):

        queryset = apply_report_scope(
            Sales.objects.all(),
            retailer=retailer,
            branch=branch,
        )

        filters = filters or {}

        if filters.get("from_date"):
            queryset = queryset.filter(created_at__date__gte=filters["from_date"])

        if filters.get("to_date"):
            queryset = queryset.filter(created_at__date__lte=filters["to_date"])

        if filters.get("customer"):
            queryset = queryset.filter(customer_id=filters["customer"])

        if filters.get("payment_status"):
            queryset = queryset.filter(payment_status=filters["payment_status"])

        summary = {
            "total_sales": get_decimal_sum(
                queryset,
                "net_amount",
            ),
            "total_paid": get_decimal_sum(
                queryset,
                "paid_amount",
            ),
            "total_due": get_decimal_sum(
                queryset,
                "due_amount",
            ),
            "invoice_count": queryset.count(),
        }

        return {
            "summary": summary,
            "data": queryset.order_by("-created_at"),
        }


# =========================
# SALES RETURN REPORT SERVICE
# =========================


class SalesReturnReportService:

    @staticmethod
    def get_report(retailer=None, branch=None):

        queryset = apply_report_scope(
            SalesReturn.objects.all(),
            retailer=retailer,
            branch=branch,
        )

        summary = {
            "total_returns": get_decimal_sum(
                queryset,
                "total_amount",
            ),
            "refund_amount": get_decimal_sum(
                queryset,
                "refund_amount",
            ),
            "return_count": queryset.count(),
        }

        return {
            "summary": summary,
            "data": queryset.order_by("-created_at"),
        }


# =========================
# STOCK ADJUSTMENT REPORT SERVICE
# =========================


class StockAdjustmentReportService:

    @staticmethod
    def get_report(retailer=None, branch=None):

        queryset = apply_report_scope(
            StockAdjustment.objects.all(),
            retailer=retailer,
            branch=branch,
        )

        return queryset.order_by("-created_at")


# =========================
# STOCK REPORT SERVICE
# =========================


class StockReportService:

    @staticmethod
    def get_report(retailer=None, branch=None):

        queryset = apply_report_scope(
            StockBatch.objects.all(),
            retailer=retailer,
            branch=branch,
        )

        summary = {
            "total_stock": get_decimal_sum(
                queryset,
                "available_qty",
            ),
            "batch_count": queryset.count(),
        }

        return {
            "summary": summary,
            "data": queryset.order_by("-created_at"),
        }


# =========================
# STOCK TRANSFER REPORT SERVICE
# =========================


class StockTransferReportService:

    @staticmethod
    def get_report(retailer=None, branch=None):

        queryset = apply_report_scope(
            StockTransfer.objects.all(),
            retailer=retailer,
            branch=branch,
        )

        return queryset.order_by("-created_at")


# =========================
# SUPPLIER LEDGER SERVICE
# =========================


class SupplierLedgerService:

    @staticmethod
    def get_supplier_ledger(
        supplier_id,
        retailer=None,
        branch=None,
    ):

        queryset = apply_report_scope(
            StockTransaction.objects.all(),
            retailer=retailer,
            branch=branch,
        )

        return queryset.filter(supplier_id=supplier_id).order_by("-created_at")

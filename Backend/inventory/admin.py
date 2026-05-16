from django.contrib import admin

from .models.stock_batch_models import StockBatch
from .models.stock_transaction_models import StockTransaction
from .models.stock_transaction_item_models import StockTransactionItem
from .models.stock_transfer_models import StockTransfer
from .models.stock_adjustment_models import StockAdjustment

from .models.sales_models import Sales
from .models.sales_item_models import SalesItem
from .models.sales_return_models import SalesReturn
from .models.sales_return_item_models import SalesReturnItem

from .models.purchase_return_models import PurchaseReturn
from .models.purchase_return_item_models import PurchaseReturnItem

from .models.payment_models import Payment
from .models.receipt_models import Receipt
from .models.expiry_damage_models import ExpiryDamage


# =========================================================
# BASE ADMIN
# =========================================================

class RetailerBranchAdmin(admin.ModelAdmin):

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    def get_queryset(self, request):

        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        return qs.filter(
            retailer=request.user.retailer
        )

    def save_model(self, request, obj, form, change):

        if not request.user.is_superuser:

            obj.retailer = request.user.retailer

            if hasattr(obj, "branch"):
                obj.branch = request.user.branch

        super().save_model(
            request,
            obj,
            form,
            change
        )


# =========================================================
# STOCK
# =========================================================

@admin.register(StockBatch)
class StockBatchAdmin(RetailerBranchAdmin):

    list_display = (
        "id",
        "retailer",
        "branch",
        "product",
        "batch_no",
        "quantity",
        "available_qty",
        "reserved_qty",
        "expiry_date",
        "is_expired",
    )

    search_fields = (
        "batch_no",
        "product__name",
    )

    list_filter = (
        "retailer",
        "branch",
        "expiry_date",
        "is_expired",
    )


@admin.register(StockTransaction)
class StockTransactionAdmin(RetailerBranchAdmin):

    list_display = (
        "id",
        "transaction_no",
        "retailer",
        "branch",
        "transaction_type",
        "supplier",
        "customer",
        "status",
        "total_amount",
        "created_at",
    )

    search_fields = (
        "transaction_no",
        "reference_no",
    )

    list_filter = (
        "retailer",
        "branch",
        "transaction_type",
        "status",
    )


@admin.register(StockTransactionItem)
class StockTransactionItemAdmin(RetailerBranchAdmin):

    list_display = (
        "id",
        "retailer",
        "branch",
        "transaction",
        "product",
        "batch",
        "movement_type",
        "qty",
        "free_qty",
        "purchase_price",
        "sale_price",
        "total_amount",
    )

    search_fields = (
        "product__name",
        "transaction__transaction_no",
    )

    list_filter = (
        "retailer",
        "branch",
        "movement_type",
        "product",
    )


@admin.register(StockTransfer)
class StockTransferAdmin(RetailerBranchAdmin):

    list_display = (
        "id",
        "transfer_no",
        "retailer",
        "from_branch",
        "to_branch",
        "product",
        "batch",
        "quantity",
        "unit_cost",
        "total_cost",
        "status",
        "created_at",
    )

    search_fields = (
        "transfer_no",
        "product__name",
    )

    list_filter = (
        "retailer",
        "from_branch",
        "to_branch",
        "status",
    )


@admin.register(StockAdjustment)
class StockAdjustmentAdmin(RetailerBranchAdmin):

    list_display = (
        "id",
        "retailer",
        "branch",
        "product",
        "batch",
        "adjustment_type",
        "adjustment_qty",
        "reason",
        "total_value",
        "created_at",
    )

    search_fields = (
        "reason",
        "reference_no",
        "product__name",
    )

    list_filter = (
        "retailer",
        "branch",
        "adjustment_type",
    )


# =========================================================
# SALES
# =========================================================

@admin.register(Sales)
class SalesAdmin(RetailerBranchAdmin):

    list_display = (
        "id",
        "invoice_no",
        "retailer",
        "branch",
        "customer",
        "total_amount",
        "discount",
        "net_amount",
        "payment_status",
        "created_at",
    )

    search_fields = (
        "invoice_no",
    )

    list_filter = (
        "retailer",
        "branch",
        "payment_status",
        "created_at",
    )


@admin.register(SalesItem)
class SalesItemAdmin(RetailerBranchAdmin):

    list_display = (
        "id",
        "retailer",
        "branch",
        "sales",
        "product",
        "batch",
        "qty",
        "unit_price",
        "amount",
    )

    search_fields = (
        "product__name",
        "sales__invoice_no",
    )

    list_filter = (
        "retailer",
        "branch",
        "created_at",
    )


@admin.register(SalesReturn)
class SalesReturnAdmin(RetailerBranchAdmin):

    list_display = (
        "id",
        "return_no",
        "retailer",
        "branch",
        "sales",
        "total_amount",
        "refund_amount",
        "status",
        "created_at",
    )

    search_fields = (
        "return_no",
    )

    list_filter = (
        "retailer",
        "branch",
        "status",
    )


@admin.register(SalesReturnItem)
class SalesReturnItemAdmin(RetailerBranchAdmin):

    list_display = (
        "id",
        "retailer",
        "branch",
        "sales_return",
        "product",
        "qty",
        "amount",
    )

    list_filter = (
        "retailer",
        "branch",
    )


# =========================================================
# PURCHASE
# =========================================================

@admin.register(PurchaseReturn)
class PurchaseReturnAdmin(RetailerBranchAdmin):

    list_display = (
        "id",
        "return_no",
        "retailer",
        "branch",
        "supplier",
        "total_amount",
        "adjusted_amount",
        "status",
        "created_at",
    )

    search_fields = (
        "return_no",
    )

    list_filter = (
        "retailer",
        "branch",
        "status",
    )


@admin.register(PurchaseReturnItem)
class PurchaseReturnItemAdmin(RetailerBranchAdmin):

    list_display = (
        "id",
        "retailer",
        "branch",
        "purchase_return",
        "product",
        "qty",
        "amount",
    )

    list_filter = (
        "retailer",
        "branch",
    )


# =========================================================
# PAYMENT / RECEIPT
# =========================================================

@admin.register(Payment)
class PaymentAdmin(RetailerBranchAdmin):

    list_display = (
        "id",
        "payment_no",
        "retailer",
        "branch",
        "supplier",
        "amount",
        "paid_amount",
        "due_amount",
        "payment_method",
        "status",
        "created_at",
    )

    search_fields = (
        "payment_no",
        "reference_no",
    )

    list_filter = (
        "retailer",
        "branch",
        "status",
        "payment_method",
    )


@admin.register(Receipt)
class ReceiptAdmin(RetailerBranchAdmin):

    list_display = (
        "id",
        "receipt_no",
        "retailer",
        "branch",
        "customer",
        "amount",
        "paid_amount",
        "due_amount",
        "payment_method",
        "status",
        "created_at",
    )

    search_fields = (
        "receipt_no",
        "reference_no",
    )

    list_filter = (
        "retailer",
        "branch",
        "status",
        "payment_method",
    )


# =========================================================
# EXPIRY / DAMAGE
# =========================================================

@admin.register(ExpiryDamage)
class ExpiryDamageAdmin(RetailerBranchAdmin):

    list_display = (
        "id",
        "retailer",
        "branch",
        "product",
        "batch",
        "issue_type",
        "quantity",
        "unit_price",
        "total_loss",
        "expiry_date",
        "created_at",
    )

    search_fields = (
        "product__name",
        "batch__batch_no",
    )

    list_filter = (
        "retailer",
        "branch",
        "issue_type",
    )
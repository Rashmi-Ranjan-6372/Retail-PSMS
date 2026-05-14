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


# ===================== STOCK =====================

@admin.register(StockBatch)
class StockBatchAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "branch",
        "batch_no",
        "quantity",
        "available_qty",
        "reserved_qty",
        "expiry_date",
    )
    search_fields = ("batch_no", "product__name")
    list_filter = ("branch", "expiry_date", "is_expired")


@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "transaction_no",
        "transaction_type",
        "branch",
        "supplier",
        "customer",
        "status",
        "total_amount",
        "created_at",
    )
    search_fields = ("transaction_no",)
    list_filter = ("transaction_type", "status", "branch")


@admin.register(StockTransactionItem)
class StockTransactionItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
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
    list_filter = ("movement_type", "product")


@admin.register(StockTransfer)
class StockTransferAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "transfer_no",
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
    list_filter = ("status", "from_branch", "to_branch")


@admin.register(StockAdjustment)
class StockAdjustmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "batch",
        "adjustment_qty",
        "reason",
        "created_at",
    )
    search_fields = ("reason",)


# ===================== SALES =====================

@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "invoice_no",
        "customer",
        "total_amount",
        "discount",
        "net_amount",
        "created_at",
    )
    search_fields = ("invoice_no",)
    list_filter = ("created_at",)


@admin.register(SalesItem)
class SalesItemAdmin(admin.ModelAdmin):

    list_display = (
        "id",
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

    list_filter = ("created_at",)


@admin.register(SalesReturn)
class SalesReturnAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "return_no",
        "sales",
        "total_amount",
        "created_at",
    )


@admin.register(SalesReturnItem)
class SalesReturnItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "sales_return",
        "product",
        "qty",
        "amount",
    )


# ===================== PURCHASE =====================

@admin.register(PurchaseReturn)
class PurchaseReturnAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "return_no",
        "supplier",
        "total_amount",
        "created_at",
    )


@admin.register(PurchaseReturnItem)
class PurchaseReturnItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "purchase_return",
        "product",
        "qty",
        "amount",
    )


# ===================== PAYMENT / RECEIPT =====================

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "supplier",
        "amount",
        "payment_method",
        "created_at",
    )
    search_fields = ("payment_method",)


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "amount",
        "payment_method",
        "created_at",
    )


# ===================== EXPIRY / DAMAGE =====================

@admin.register(ExpiryDamage)
class ExpiryDamageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "batch",
        "branch",
        "issue_type",
        "quantity",
        "unit_price",
        "total_loss",
        "expiry_date",
        "created_at",
    )
    list_filter = ("issue_type", "branch")
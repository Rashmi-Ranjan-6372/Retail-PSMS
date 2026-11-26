import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from inventory.models.sales_models import Sales
from inventory.models.stock_batch_models import StockBatch
from inventory.models.payment_models import Payment
from inventory.models.receipt_models import Receipt


logger = logging.getLogger(__name__)

LOW_STOCK_LIMIT = 10


# ============================================================
# SALES CREATED SIGNAL
# ============================================================

@receiver(
    post_save,
    sender=Sales,
    dispatch_uid="reports_sales_created_signal"
)
def sales_created_signal(sender, instance, created, **kwargs):

    if not created:
        return

    logger.info(
        "New Sales Invoice Created | "
        "Invoice: %s | Retailer: %s | Branch: %s | Amount: %s",
        instance.invoice_no,
        instance.retailer_id,
        instance.branch_id,
        instance.net_amount
    )


# ============================================================
# LOW STOCK ALERT SIGNAL
# ============================================================

@receiver(
    post_save,
    sender=StockBatch,
    dispatch_uid="reports_low_stock_alert_signal"
)
def low_stock_alert_signal(sender, instance, created, **kwargs):

    if instance.available_qty > LOW_STOCK_LIMIT:
        return

    if created:
        logger.warning(
            "LOW STOCK ALERT | "
            "Product: %s | Batch: %s | "
            "Retailer: %s | Branch: %s | Available Qty: %s",
            instance.product.name,
            instance.batch_no,
            instance.retailer_id,
            instance.branch_id,
            instance.available_qty
        )


# ============================================================
# EXPIRED STOCK ALERT SIGNAL
# ============================================================

@receiver(
    post_save,
    sender=StockBatch,
    dispatch_uid="reports_expired_stock_signal"
)
def expired_stock_signal(sender, instance, created, **kwargs):

    if not created:
        return

    if not instance.is_expired:
        return

    logger.warning(
        "EXPIRED STOCK ALERT | "
        "Product: %s | Batch: %s | "
        "Retailer: %s | Branch: %s | Expiry Date: %s",
        instance.product.name,
        instance.batch_no,
        instance.retailer_id,
        instance.branch_id,
        instance.expiry_date
    )


# ============================================================
# PAYMENT CREATED SIGNAL
# ============================================================

@receiver(
    post_save,
    sender=Payment,
    dispatch_uid="reports_payment_created_signal"
)
def payment_signal(sender, instance, created, **kwargs):

    if not created:
        return

    logger.info(
        "Payment Created | "
        "Payment No: %s | Retailer: %s | Branch: %s | Amount: %s",
        instance.payment_no,
        instance.retailer_id,
        instance.branch_id,
        instance.amount
    )


# ============================================================
# RECEIPT CREATED SIGNAL
# ============================================================

@receiver(
    post_save,
    sender=Receipt,
    dispatch_uid="reports_receipt_created_signal"
)
def receipt_signal(sender, instance, created, **kwargs):

    if not created:
        return

    logger.info(
        "Receipt Created | "
        "Receipt No: %s | Retailer: %s | Branch: %s",
        instance.receipt_no,
        instance.retailer_id,
        instance.branch_id
    )

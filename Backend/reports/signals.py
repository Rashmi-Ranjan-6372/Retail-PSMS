from django.db.models.signals import post_save
from django.dispatch import receiver

from inventory.models.sales_models import Sales
from inventory.models.stock_batch_models import StockBatch
from inventory.models.payment_models import Payment
from inventory.models.receipt_models import Receipt

import logging

logger = logging.getLogger(__name__)


# ==========================================
# SALES CREATED SIGNAL
# ==========================================

@receiver(post_save, sender=Sales)
def sales_created_signal(sender, instance, created, **kwargs):

    if created:

        logger.info(
            f"New Sales Invoice Created : "
            f"{instance.invoice_no}"
        )


# ==========================================
# LOW STOCK ALERT SIGNAL
# ==========================================

@receiver(post_save, sender=StockBatch)
def low_stock_alert_signal(sender, instance, **kwargs):

    LOW_STOCK_LIMIT = 10

    if instance.available_qty <= LOW_STOCK_LIMIT:

        logger.warning(
            f"Low Stock Alert : "
            f"{instance.product.name} | "
            f"Available Qty : {instance.available_qty}"
        )


# ==========================================
# EXPIRED STOCK ALERT SIGNAL
# ==========================================

@receiver(post_save, sender=StockBatch)
def expired_stock_signal(sender, instance, **kwargs):

    if instance.is_expired:

        logger.warning(
            f"Expired Stock : "
            f"{instance.product.name} | "
            f"Batch : {instance.batch_no}"
        )


# ==========================================
# PAYMENT CREATED SIGNAL
# ==========================================

@receiver(post_save, sender=Payment)
def payment_signal(sender, instance, created, **kwargs):

    if created:

        logger.info(
            f"Payment Created : "
            f"{instance.payment_no}"
        )


# ==========================================
# RECEIPT CREATED SIGNAL
# ==========================================

@receiver(post_save, sender=Receipt)
def receipt_signal(sender, instance, created, **kwargs):

    if created:

        logger.info(
            f"Receipt Created : "
            f"{instance.receipt_no}"
        )
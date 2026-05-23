from django.db.models.signals import (
    post_save,
    post_delete,
)

from django.dispatch import receiver

# =====================================================
# SALES ITEM SIGNALS
# =====================================================

from inventory.models.sales_item_models import (
    SalesItem
)

from inventory.models.stock_batch_models import (
    StockBatch
)

from inventory.services.sales_service import (
    update_sales_totals
)


# =====================================================
# UPDATE SALES TOTAL AFTER SAVE
# =====================================================

@receiver(post_save, sender=SalesItem)
def update_sales_after_save(
    sender,
    instance,
    created,
    **kwargs
):

    update_sales_totals(
        instance.sales
    )


# =====================================================
# RESTORE STOCK AFTER SALES ITEM DELETE
# =====================================================

@receiver(post_delete, sender=SalesItem)
def restore_stock_after_sales_delete(
    sender,
    instance,
    **kwargs
):

    batch = instance.batch

    batch.available_qty += (
        instance.qty +
        instance.free_qty
    )

    batch.save()

    update_sales_totals(
        instance.sales
    )


# =====================================================
# SALES RETURN ITEM SIGNALS
# =====================================================

from inventory.models.sales_return_item_models import (
    SalesReturnItem
)

from inventory.services.sales_return_service import (
    process_sales_return
)


# =====================================================
# PROCESS SALES RETURN
# =====================================================

@receiver(post_save, sender=SalesReturnItem)
def process_return_after_save(
    sender,
    instance,
    created,
    **kwargs
):

    process_sales_return(
        instance.sales_return
    )


# =====================================================
# PURCHASE RETURN ITEM SIGNALS
# =====================================================

from inventory.models.purchase_return_item_models import (
    PurchaseReturnItem
)

from inventory.services.purchase_return_service import (
    update_purchase_return_totals
)


# =====================================================
# UPDATE PURCHASE RETURN TOTAL
# =====================================================

@receiver(post_save, sender=PurchaseReturnItem)
def update_purchase_return_after_save(
    sender,
    instance,
    created,
    **kwargs
):

    update_purchase_return_totals(
        instance.purchase_return
    )


# =====================================================
# STOCK TRANSFER SIGNALS
# =====================================================

from inventory.models.stock_transfer_models import (
    StockTransfer
)

from inventory.services.stock_transfer_service import (
    process_stock_transfer
)


# =====================================================
# PROCESS STOCK TRANSFER
# =====================================================

@receiver(post_save, sender=StockTransfer)
def process_transfer_after_save(
    sender,
    instance,
    created,
    **kwargs
):

    if instance.status == "APPROVED":

        process_stock_transfer(
            instance
        )


# =====================================================
# STOCK ADJUSTMENT SIGNALS
# =====================================================

from inventory.models.stock_adjustment_models import (
    StockAdjustment
)

from inventory.services.stock_adjustment_service import (
    process_stock_adjustment
)


# =====================================================
# PROCESS STOCK ADJUSTMENT
# =====================================================

@receiver(post_save, sender=StockAdjustment)
def process_adjustment_after_save(
    sender,
    instance,
    created,
    **kwargs
):

    process_stock_adjustment(
        instance
    )


# =====================================================
# PAYMENT SIGNALS
# =====================================================

from inventory.models.payment_models import (
    Payment
)

from inventory.services.payment_service import (
    update_payment_status
)


# =====================================================
# UPDATE PAYMENT STATUS
# =====================================================

@receiver(post_save, sender=Payment)
def update_payment_after_save(
    sender,
    instance,
    created,
    **kwargs
):

    update_payment_status(
        instance
    )


# =====================================================
# RECEIPT SIGNALS
# =====================================================

from inventory.models.receipt_models import (
    Receipt
)

from inventory.services.receipt_service import (
    update_receipt_status
)


# =====================================================
# UPDATE RECEIPT STATUS
# =====================================================

@receiver(post_save, sender=Receipt)
def update_receipt_after_save(
    sender,
    instance,
    created,
    **kwargs
):

    update_receipt_status(
        instance
    )
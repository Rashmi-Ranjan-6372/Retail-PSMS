from decimal import Decimal

from django.db import transaction

from inventory.models.sales_models import (
    Sales
)

from inventory.models.sales_return_models import (
    SalesReturn
)

from inventory.models.sales_return_item_models import (
    SalesReturnItem
)

from inventory.models.stock_batch_models import (
    StockBatch
)

from subscriptions.utils import (
    check_subscription_write_access,
    validate_branch_subscription
)


# =====================================================
# PROCESS SALES RETURN
# =====================================================

@transaction.atomic
def process_sales_return(
    sales_return_id
):

    # =====================================================
    # LOCK SALES RETURN
    # =====================================================

    sales_return = (
        SalesReturn.objects
        .select_for_update()
        .select_related("sales")
        .get(id=sales_return_id)
    )

    check_subscription_write_access(
        sales_return.retailer
    )

    validate_branch_subscription(
        sales_return.retailer
    )

    # =====================================================
    # PREVENT DOUBLE PROCESSING
    # =====================================================

    if sales_return.status == "COMPLETED":

        raise ValueError(
            "Sales return already processed"
        )

    total_return_amount = Decimal("0.00")

    # =====================================================
    # GET RETURN ITEMS
    # =====================================================

    items = (
        SalesReturnItem.objects
        .select_related(
            "batch",
            "product",
        )
        .filter(
            sales_return=sales_return
        )
    )

    # =====================================================
    # PROCESS EACH ITEM
    # =====================================================

    for item in items:

        batch = (
            StockBatch.objects
            .select_for_update()
            .get(id=item.batch.id)
        )

        return_qty = (
            item.qty +
            item.free_qty
        )

        # =====================================================
        # RESTORE STOCK
        # =====================================================

        batch.available_qty += return_qty

        batch.save(
            update_fields=[
                "available_qty"
            ]
        )

        # =====================================================
        # CALCULATE RETURN AMOUNT
        # =====================================================

        total_return_amount += Decimal(
            str(item.amount or 0)
        )

    # =====================================================
    # UPDATE SALES RETURN
    # =====================================================

    sales_return.total_amount = (
        total_return_amount
    )

    sales_return.refund_amount = (
        total_return_amount
    )

    sales_return.status = "COMPLETED"

    sales_return.save(
        update_fields=[
            "total_amount",
            "refund_amount",
            "status"
        ]
    )

    # =====================================================
    # UPDATE ORIGINAL SALES
    # =====================================================

    sales = (
        Sales.objects
        .select_for_update()
        .get(id=sales_return.sales.id)
    )

    sales.total_amount = (
        Decimal(str(sales.total_amount))
        - total_return_amount
    )

    # =====================================================
    # PREVENT NEGATIVE VALUE
    # =====================================================

    if sales.total_amount < 0:

        sales.total_amount = Decimal(
            "0.00"
        )

    # =====================================================
    # RECALCULATE NET AMOUNT
    # =====================================================

    sales.net_amount = (
        Decimal(str(sales.total_amount))
        - Decimal(str(sales.discount or 0))
    )

    if sales.net_amount < 0:

        sales.net_amount = Decimal(
            "0.00"
        )

    # =====================================================
    # RECALCULATE DUE
    # =====================================================

    sales.due_amount = (
        sales.net_amount
        - Decimal(str(sales.paid_amount or 0))
    )

    # =====================================================
    # PAYMENT STATUS
    # =====================================================

    if sales.due_amount <= 0:

        sales.payment_status = "PAID"

    elif sales.paid_amount > 0:

        sales.payment_status = "PARTIAL"

    else:

        sales.payment_status = "UNPAID"

    sales.save(
        update_fields=[
            "total_amount",
            "net_amount",
            "due_amount",
            "payment_status"
        ]
    )

    return sales_return
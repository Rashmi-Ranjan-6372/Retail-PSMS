from decimal import Decimal

from django.db import transaction

from inventory.models.stock_transaction_models import (
    StockTransaction
)

from inventory.models.stock_transaction_item_models import (
    StockTransactionItem
)

from inventory.models.stock_batch_models import (
    StockBatch
)


# =====================================================
# CREATE PURCHASE
# =====================================================

@transaction.atomic
def create_purchase(
    *,
    retailer,
    branch,
    supplier,
    items,
    created_by,
    remarks=None,
):

    total_amount = Decimal("0.00")

    # =====================================================
    # CREATE STOCK TRANSACTION
    # =====================================================

    purchase = StockTransaction.objects.create(
        retailer=retailer,
        branch=branch,
        supplier=supplier,
        transaction_type="PURCHASE",
        remarks=remarks,
        created_by=created_by,
    )

    # =====================================================
    # PROCESS ITEMS
    # =====================================================

    for item in items:

        product = item["product"]

        qty = int(item["qty"])

        free_qty = int(
            item.get("free_qty", 0)
        )

        batch_no = item["batch_no"]

        purchase_price = Decimal(
            str(item["purchase_price"])
        )

        sale_price = Decimal(
            str(item["sale_price"])
        )

        mrp = Decimal(
            str(item.get("mrp", 0))
        )

        expiry_date = item["expiry_date"]

        manufacture_date = item.get(
            "manufacture_date"
        )

        total_qty = qty + free_qty

        # =====================================================
        # FIND OR CREATE BATCH
        # =====================================================

        batch, created = (
            StockBatch.objects
            .select_for_update()
            .get_or_create(
                retailer=retailer,
                branch=branch,
                product=product,
                batch_no=batch_no,

                defaults={
                    "supplier": supplier,
                    "quantity": total_qty,
                    "available_qty": total_qty,
                    "purchase_price": purchase_price,
                    "sale_price": sale_price,
                    "mrp": mrp,
                    "expiry_date": expiry_date,
                    "manufacture_date": manufacture_date,
                    "created_by": created_by,
                }
            )
        )

        # =====================================================
        # UPDATE EXISTING BATCH
        # =====================================================

        if not created:

            batch.quantity += total_qty

            batch.available_qty += total_qty

            batch.purchase_price = purchase_price

            batch.sale_price = sale_price

            batch.mrp = mrp

            batch.expiry_date = expiry_date

            batch.manufacture_date = (
                manufacture_date
            )

            batch.save()

        # =====================================================
        # ITEM TOTAL
        # =====================================================

        item_total = (
            Decimal(str(qty))
            * purchase_price
        )

        total_amount += item_total

        # =====================================================
        # CREATE TRANSACTION ITEM
        # =====================================================

        StockTransactionItem.objects.create(
            retailer=retailer,
            branch=branch,

            transaction=purchase,

            product=product,

            batch=batch,

            movement_type="IN",

            qty=qty,

            free_qty=free_qty,

            purchase_price=purchase_price,

            sale_price=sale_price,

            expiry_date=expiry_date,

            total_amount=item_total,

            available_after=batch.available_qty,

            created_by=created_by,
        )

    # =====================================================
    # UPDATE TOTAL
    # =====================================================

    purchase.total_amount = total_amount

    purchase.save()

    return purchase
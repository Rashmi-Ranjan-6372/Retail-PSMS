from decimal import Decimal

from django.db import transaction

from inventory.models.sales_models import (
    Sales
)

from inventory.models.sales_item_models import (
    SalesItem
)

from inventory.models.stock_batch_models import (
    StockBatch
)

from inventory.utils.expiry_checker import (
    is_batch_expired
)


@transaction.atomic
def create_sale(
    *,
    retailer,
    branch,
    customer,
    items,
    paid_amount,
    created_by,
    discount=0,
    remarks=None,
):

    total_amount = Decimal("0.00")

    paid_amount = Decimal(str(paid_amount or 0))

    discount = Decimal(str(discount or 0))

    # =====================================================
    # CREATE SALE
    # =====================================================

    sale = Sales.objects.create(
        retailer=retailer,
        branch=branch,
        customer=customer,
        paid_amount=paid_amount,
        discount=discount,
        remarks=remarks,
        created_by=created_by,
    )

    # =====================================================
    # CREATE SALES ITEMS
    # =====================================================

    for item in items:

        batch = (
            StockBatch.objects
            .select_for_update()
            .get(
                id=item["batch"],
                retailer=retailer
            )
        )

        qty = int(item.get("qty", 0))

        free_qty = int(
            item.get("free_qty", 0)
        )

        item_discount = Decimal(
            str(item.get("discount", 0))
        )

        tax_percent = Decimal(
            str(item.get("tax_percent", 0))
        )

        # =====================================================
        # BRANCH VALIDATION
        # =====================================================

        if batch.branch != branch:

            raise ValueError(
                f"{batch.product.name} "
                f"does not belong to this branch"
            )

        # =====================================================
        # EXPIRY VALIDATION
        # =====================================================

        if (
            batch.is_expired or
            is_batch_expired(batch)
        ):

            raise ValueError(
                f"{batch.product.name} "
                f"batch is expired"
            )

        # =====================================================
        # STOCK VALIDATION
        # =====================================================

        total_required_qty = (
            qty + free_qty
        )

        if (
            batch.available_qty <
            total_required_qty
        ):

            raise ValueError(
                f"Insufficient stock for "
                f"{batch.product.name}"
            )

        # =====================================================
        # STOCK DEDUCTION
        # =====================================================

        batch.available_qty -= (
            total_required_qty
        )

        batch.save(
            update_fields=["available_qty"]
        )

        # =====================================================
        # ITEM CALCULATIONS
        # =====================================================

        unit_price = batch.sale_price

        base_amount = (
            Decimal(str(qty)) *
            Decimal(str(unit_price))
        )

        discounted_amount = (
            base_amount -
            item_discount
        )

        tax_amount = (
            discounted_amount *
            tax_percent
        ) / Decimal("100")

        final_amount = (
            discounted_amount +
            tax_amount
        )

        total_amount += final_amount

        # =====================================================
        # CREATE SALES ITEM
        # =====================================================

        SalesItem.objects.create(
            retailer=retailer,
            branch=branch,
            sales=sale,
            product=batch.product,
            batch=batch,

            qty=qty,
            free_qty=free_qty,

            unit_price=unit_price,

            discount=item_discount,

            tax_percent=tax_percent,

            tax_amount=tax_amount,

            amount=final_amount,

            created_by=created_by,
        )

    # =====================================================
    # UPDATE SALE TOTAL
    # =====================================================

    sale.total_amount = total_amount

    sale.save()

    return sale

# =====================================================
# UPDATE SALES TOTALS
# =====================================================

def update_sales_totals(sale):

    items = sale.items.all()

    total_amount = Decimal("0.00")

    for item in items:

        total_amount += (
            item.amount or Decimal("0.00")
        )

    sale.total_amount = total_amount

    sale.save(
        update_fields=[
            "total_amount",
            "net_amount",
            "due_amount",
            "payment_status",
        ]
    )

    return sale
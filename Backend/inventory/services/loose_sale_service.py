from decimal import Decimal

from inventory.models.sales_item_models import (
    SalesItem
)


class LooseSaleService:

    # =====================================================
    # CALCULATE ITEM AMOUNT
    # =====================================================

    @staticmethod
    def calculate_item_amount(
        qty,
        unit_price,
        discount=0,
        tax_percent=0
    ):

        qty = Decimal(qty or 0)

        unit_price = Decimal(unit_price or 0)

        discount = Decimal(discount or 0)

        tax_percent = Decimal(tax_percent or 0)

        # =========================
        # BASE AMOUNT
        # =========================

        base_amount = (
            qty * unit_price
        )

        # =========================
        # AFTER DISCOUNT
        # =========================

        discounted_amount = (
            base_amount - discount
        )

        # =========================
        # TAX CALCULATION
        # =========================

        tax_amount = (
            discounted_amount *
            tax_percent
        ) / Decimal("100")

        # =========================
        # FINAL AMOUNT
        # =========================

        final_amount = (
            discounted_amount +
            tax_amount
        )

        return {
            "base_amount": round(base_amount, 2),
            "discounted_amount": round(discounted_amount, 2),
            "tax_amount": round(tax_amount, 2),
            "final_amount": round(final_amount, 2),
        }

    # =====================================================
    # CREATE SALES ITEM
    # =====================================================

    @staticmethod
    def create_sales_item(
        *,
        retailer,
        branch,
        sales,
        product,
        batch,
        qty,
        unit_price,
        discount=0,
        tax_percent=0,
        free_qty=0,
        created_by=None
    ):

        calculation = (
            LooseSaleService.calculate_item_amount(
                qty=qty,
                unit_price=unit_price,
                discount=discount,
                tax_percent=tax_percent
            )
        )

        sales_item = SalesItem.objects.create(
            retailer=retailer,
            branch=branch,
            sales=sales,
            product=product,
            batch=batch,
            qty=qty,
            free_qty=free_qty,
            unit_price=unit_price,
            discount=discount,
            tax_percent=tax_percent,
            tax_amount=calculation["tax_amount"],
            amount=calculation["final_amount"],
            created_by=created_by,
        )

        return sales_item
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from django.db import transaction

from inventory.models.sales_item_models import SalesItem
from inventory.models.stock_batch_models import StockBatch

from subscriptions.utils import (
    check_subscription_write_access,
    validate_branch_subscription,
)


class LooseSaleService:

    # =====================================================
    # DECIMAL CONVERSION
    # =====================================================

    @staticmethod
    def to_decimal(value, field_name):

        try:
            return Decimal(str(value if value is not None else 0))
        except (InvalidOperation, TypeError, ValueError):
            raise ValueError(f"{field_name} must be a valid number.")

    # =====================================================
    # CALCULATE ITEM AMOUNT
    # =====================================================

    @staticmethod
    def calculate_item_amount(qty, unit_price, discount=0, tax_percent=0):

        qty = LooseSaleService.to_decimal(qty, "Quantity")
        unit_price = LooseSaleService.to_decimal(unit_price, "Unit price")
        discount = LooseSaleService.to_decimal(discount, "Discount")
        tax_percent = LooseSaleService.to_decimal(tax_percent, "Tax percentage")

        if qty <= 0:
            raise ValueError("Quantity must be greater than 0.")

        if unit_price < 0:
            raise ValueError("Unit price cannot be negative.")

        if discount < 0:
            raise ValueError("Discount cannot be negative.")

        if tax_percent < 0:
            raise ValueError("Tax percentage cannot be negative.")

        base_amount = qty * unit_price

        if discount > base_amount:
            raise ValueError("Discount cannot be greater than the base amount.")

        discounted_amount = base_amount - discount

        tax_amount = (discounted_amount * tax_percent) / Decimal("100")

        final_amount = discounted_amount + tax_amount

        return {
            "base_amount": base_amount.quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            ),
            "discounted_amount": discounted_amount.quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            ),
            "tax_amount": tax_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            "final_amount": final_amount.quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            ),
        }

    # =====================================================
    # CREATE SALES ITEM
    # =====================================================

    @staticmethod
    @transaction.atomic
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
        created_by=None,
    ):

        if not retailer:
            raise ValueError("Retailer is required.")

        if not branch:
            raise ValueError("Branch is required.")

        if not sales:
            raise ValueError("Sales record is required.")

        if not product:
            raise ValueError("Product is required.")

        if not batch:
            raise ValueError("Stock batch is required.")

        check_subscription_write_access(retailer)
        validate_branch_subscription(retailer)

        try:
            qty = int(qty)
            free_qty = int(free_qty or 0)
        except (TypeError, ValueError):
            raise ValueError("Quantity and free quantity must be valid integers.")

        if qty <= 0:
            raise ValueError("Quantity must be greater than 0.")

        if free_qty < 0:
            raise ValueError("Free quantity cannot be negative.")

        # Validate retailer and branch ownership.

        if branch.retailer_id != retailer.id:
            raise ValueError("Branch does not belong to this retailer.")

        if sales.retailer_id != retailer.id:
            raise ValueError("Sales record does not belong to this retailer.")

        if sales.branch_id != branch.id:
            raise ValueError("Sales record does not belong to this branch.")

        if product.retailer_id != retailer.id:
            raise ValueError("Product does not belong to this retailer.")

        # Lock and fetch the latest batch stock.

        try:
            batch = StockBatch.objects.select_for_update().get(
                id=batch.id, retailer=retailer, branch=branch, product=product
            )
        except StockBatch.DoesNotExist:
            raise ValueError(
                "Selected batch does not belong to this product " "and branch."
            )

        # Validate expiry.

        from django.utils import timezone

        if batch.is_expired or (
            batch.expiry_date and batch.expiry_date < timezone.localdate()
        ):
            raise ValueError("Cannot sell an expired batch.")

        total_quantity = qty + free_qty

        if batch.available_qty < total_quantity:
            raise ValueError(
                f"Insufficient available stock in batch " f"{batch.batch_no}."
            )

        if batch.quantity < total_quantity:
            raise ValueError(f"Insufficient total stock in batch " f"{batch.batch_no}.")

        # Calculate item amount.
        # Free quantity is not charged.

        calculation = LooseSaleService.calculate_item_amount(
            qty=qty, unit_price=unit_price, discount=discount, tax_percent=tax_percent
        )

        # Deduct sold quantity and free quantity.

        batch.available_qty -= total_quantity
        batch.quantity -= total_quantity

        batch.save(update_fields=["available_qty", "quantity"])

        # Create sales item.

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

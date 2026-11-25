from decimal import Decimal, InvalidOperation

from django.db import transaction

from inventory.models.sales_models import Sales
from inventory.models.sales_item_models import SalesItem
from inventory.models.stock_batch_models import StockBatch

from inventory.utils.expiry_checker import is_batch_expired

from subscriptions.utils import (
    check_subscription_write_access,
    validate_branch_subscription,
)

from accounts.views import create_audit_log

# =====================================================
# DECIMAL VALIDATION
# =====================================================


def get_decimal(value, field_name):

    try:
        value = Decimal(str(value if value is not None else 0))
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError(f"Invalid {field_name}.")

    if not value.is_finite():
        raise ValueError(f"Invalid {field_name}.")

    return value


# =====================================================
# PAYMENT STATUS
# =====================================================


def calculate_payment_status(net_amount, paid_amount):

    due_amount = max(Decimal("0.00"), net_amount - paid_amount)

    if due_amount == 0:
        payment_status = "PAID"

    elif paid_amount > 0:
        payment_status = "PARTIAL"

    else:
        payment_status = "UNPAID"

    return due_amount, payment_status


# =====================================================
# CREATE SALE
# =====================================================


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
    request=None,
):

    # =====================================================
    # SUBSCRIPTION VALIDATION
    # =====================================================

    if not created_by.is_superuser:

        check_subscription_write_access(retailer)

        validate_branch_subscription(branch)

    # =====================================================
    # VALIDATE RETAILER AND BRANCH
    # =====================================================

    if not branch or branch.retailer_id != retailer.id:
        raise ValueError("Branch does not belong to this retailer.")

    # =====================================================
    # VALIDATE CUSTOMER
    # =====================================================

    if customer and customer.retailer_id != retailer.id:
        raise ValueError("Customer does not belong to this retailer.")

    # =====================================================
    # VALIDATE INPUT
    # =====================================================

    if not items:
        raise ValueError("Sale must contain at least one item.")

    paid_amount = get_decimal(paid_amount, "paid amount")

    discount = get_decimal(discount, "sale discount")

    if paid_amount < 0:
        raise ValueError("Paid amount cannot be negative.")

    if discount < 0:
        raise ValueError("Sale discount cannot be negative.")

    # =====================================================
    # VALIDATE ITEMS AND LOCK BATCHES
    # =====================================================

    validated_items = []
    total_amount = Decimal("0.00")

    for item in items:

        try:
            batch_id = item["batch"]
        except (KeyError, TypeError):
            raise ValueError("Batch ID is required for every sale item.")

        try:
            batch = (
                StockBatch.objects.select_for_update()
                .select_related("product")
                .get(id=batch_id, retailer=retailer)
            )
        except StockBatch.DoesNotExist:
            raise ValueError(f"Stock batch {batch_id} not found.")

        if batch.branch_id != branch.id:
            raise ValueError(f"{batch.product.name} does not belong to this branch.")

        if batch.is_expired or is_batch_expired(batch):
            raise ValueError(f"{batch.product.name} batch is expired.")

        # =============================================
        # QUANTITY VALIDATION
        # =============================================

        try:
            qty = int(item.get("qty", 0))
            free_qty = int(item.get("free_qty", 0))
        except (TypeError, ValueError):
            raise ValueError("Quantity and free quantity must be valid integers.")

        if qty <= 0:
            raise ValueError(
                f"Sale quantity must be greater than zero for {batch.product.name}."
            )

        if free_qty < 0:
            raise ValueError("Free quantity cannot be negative.")

        total_required_qty = qty + free_qty

        if batch.available_qty < total_required_qty:
            raise ValueError(f"Insufficient stock for {batch.product.name}.")

        # =============================================
        # PRICE AND DISCOUNT VALIDATION
        # =============================================

        unit_price = get_decimal(batch.sale_price, "unit price")

        item_discount = get_decimal(item.get("discount", 0), "item discount")

        tax_percent = get_decimal(item.get("tax_percent", 0), "tax percentage")

        if unit_price < 0:
            raise ValueError("Unit price cannot be negative.")

        if item_discount < 0:
            raise ValueError("Item discount cannot be negative.")

        if tax_percent < 0:
            raise ValueError("Tax percentage cannot be negative.")

        # =============================================
        # CALCULATE ITEM AMOUNT
        # =============================================

        base_amount = Decimal(qty) * unit_price

        if item_discount > base_amount:
            raise ValueError(
                f"Item discount cannot exceed item amount for {batch.product.name}."
            )

        discounted_amount = base_amount - item_discount

        tax_amount = discounted_amount * tax_percent / Decimal("100")

        final_amount = discounted_amount + tax_amount

        total_amount += final_amount

        validated_items.append(
            {
                "batch": batch,
                "qty": qty,
                "free_qty": free_qty,
                "total_required_qty": total_required_qty,
                "unit_price": unit_price,
                "discount": item_discount,
                "tax_percent": tax_percent,
                "tax_amount": tax_amount,
                "amount": final_amount,
            }
        )

    # =====================================================
    # CALCULATE SALE TOTALS
    # =====================================================

    if discount > total_amount:
        raise ValueError("Sale discount cannot exceed the total amount.")

    net_amount = max(Decimal("0.00"), total_amount - discount)

    if paid_amount > net_amount:
        raise ValueError("Paid amount cannot exceed the net sale amount.")

    due_amount, payment_status = calculate_payment_status(net_amount, paid_amount)

    # =====================================================
    # CREATE SALE
    # =====================================================

    sale = Sales.objects.create(
        retailer=retailer,
        branch=branch,
        customer=customer,
        total_amount=total_amount,
        discount=discount,
        net_amount=net_amount,
        paid_amount=paid_amount,
        due_amount=due_amount,
        payment_status=payment_status,
        remarks=remarks,
        created_by=created_by,
    )

    # =====================================================
    # DEDUCT STOCK AND CREATE SALE ITEMS
    # =====================================================

    for data in validated_items:

        batch = data["batch"]

        total_required_qty = data["total_required_qty"]

        batch.quantity -= total_required_qty
        batch.available_qty -= total_required_qty

        batch.save(update_fields=["quantity", "available_qty", "updated_at"])

        SalesItem.objects.create(
            retailer=retailer,
            branch=branch,
            sales=sale,
            product=batch.product,
            batch=batch,
            qty=data["qty"],
            free_qty=data["free_qty"],
            unit_price=data["unit_price"],
            discount=data["discount"],
            tax_percent=data["tax_percent"],
            tax_amount=data["tax_amount"],
            amount=data["amount"],
            created_by=created_by,
        )

    # =====================================================
    # AUDIT LOG
    # =====================================================

    if request:

        create_audit_log(
            user=created_by,
            action="create",
            model_name="Sales",
            object_id=sale.id,
            description=(f"Created Sale {sale.id} " f"Amount: {sale.total_amount}"),
            request=request,
        )

    return sale


# =====================================================
# UPDATE SALES TOTALS
# =====================================================


@transaction.atomic
def update_sales_totals(sale, request=None):

    # =====================================================
    # LOCK SALE
    # =====================================================

    try:
        sale = Sales.objects.select_for_update().get(id=sale.id)
    except Sales.DoesNotExist:
        raise ValueError("Sales invoice not found.")

    check_subscription_write_access(sale.retailer)

    validate_branch_subscription(sale.branch)

    # =====================================================
    # CALCULATE ITEM TOTAL
    # =====================================================

    items = SalesItem.objects.filter(sales=sale)

    total_amount = Decimal("0.00")

    for item in items:

        total_amount += get_decimal(item.amount, "item amount")

    # =====================================================
    # RECALCULATE SALE TOTALS
    # =====================================================

    discount = get_decimal(sale.discount, "sale discount")

    paid_amount = get_decimal(sale.paid_amount, "paid amount")

    if discount < 0 or discount > total_amount:
        raise ValueError("Sale discount is invalid for the current item total.")

    if paid_amount < 0:
        raise ValueError("Paid amount cannot be negative.")

    net_amount = max(Decimal("0.00"), total_amount - discount)

    due_amount, payment_status = calculate_payment_status(net_amount, paid_amount)

    old_amount = sale.total_amount

    sale.total_amount = total_amount
    sale.net_amount = net_amount
    sale.due_amount = due_amount
    sale.payment_status = payment_status

    sale.save(
        update_fields=[
            "total_amount",
            "net_amount",
            "due_amount",
            "payment_status",
        ]
    )

    # =====================================================
    # AUDIT LOG
    # =====================================================

    if request:

        create_audit_log(
            user=request.user,
            action="update",
            model_name="Sales",
            object_id=sale.id,
            description=(
                f"Updated Sale Totals from {old_amount} " f"to {sale.total_amount}"
            ),
            request=request,
        )

    return sale

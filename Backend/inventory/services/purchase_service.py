from decimal import Decimal, InvalidOperation

from django.db import transaction
from django.utils import timezone

from inventory.models.stock_transaction_models import StockTransaction
from inventory.models.stock_transaction_item_models import StockTransactionItem
from inventory.models.stock_batch_models import StockBatch

from subscriptions.utils import (
    check_subscription_write_access,
    validate_branch_subscription,
)

# =====================================================
# VALIDATE DECIMAL
# =====================================================


def validate_decimal(value, field_name):

    try:
        value = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError(f"{field_name} must be a valid number.")

    if not value.is_finite():
        raise ValueError(f"{field_name} must be a finite number.")

    if value < 0:
        raise ValueError(f"{field_name} cannot be negative.")

    return value


# =====================================================
# VALIDATE PURCHASE ITEM
# =====================================================


def validate_purchase_item(item, retailer, branch):

    product = item.get("product")

    if not product:
        raise ValueError("Product is required.")

    if product.retailer_id != retailer.id:
        raise ValueError(f"Product {product} does not belong to this retailer.")

    if not product.is_active:
        raise ValueError(f"Product {product} is inactive.")

    try:
        qty = int(item.get("qty"))
        free_qty = int(item.get("free_qty", 0))
    except (TypeError, ValueError):
        raise ValueError("Purchase quantity and free quantity must be integers.")

    if qty <= 0:
        raise ValueError("Purchase quantity must be greater than 0.")

    if free_qty < 0:
        raise ValueError("Free quantity cannot be negative.")

    batch_no = item.get("batch_no")

    if not batch_no or not str(batch_no).strip():
        raise ValueError("Batch number is required.")

    purchase_price = validate_decimal(item.get("purchase_price"), "Purchase price")

    sale_price = validate_decimal(item.get("sale_price"), "Sale price")

    mrp = validate_decimal(item.get("mrp"), "MRP")

    if mrp <= 0:
        raise ValueError("MRP must be greater than 0.")

    if sale_price > mrp:
        raise ValueError("Sale price cannot be greater than MRP.")

    expiry_date = item.get("expiry_date")

    if not expiry_date:
        raise ValueError("Expiry date is required.")

    if expiry_date < timezone.localdate():
        raise ValueError(f"Cannot purchase expired batch {batch_no}.")

    manufacture_date = item.get("manufacture_date")

    if manufacture_date and manufacture_date > expiry_date:
        raise ValueError("Manufacture date cannot be after expiry date.")

    return {
        "product": product,
        "qty": qty,
        "free_qty": free_qty,
        "batch_no": str(batch_no).strip(),
        "purchase_price": purchase_price,
        "sale_price": sale_price,
        "mrp": mrp,
        "expiry_date": expiry_date,
        "manufacture_date": manufacture_date,
        "total_qty": qty + free_qty,
    }


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

    # =====================================================
    # SUBSCRIPTION VALIDATION
    # =====================================================

    check_subscription_write_access(retailer)
    validate_branch_subscription(retailer)

    # =====================================================
    # RETAILER / BRANCH VALIDATION
    # =====================================================

    if not branch:
        raise ValueError("Branch is required.")

    if branch.retailer_id != retailer.id:
        raise ValueError("Branch does not belong to this retailer.")

    if not supplier:
        raise ValueError("Supplier is required.")

    if supplier.retailer_id != retailer.id:
        raise ValueError("Supplier does not belong to this retailer.")

    if not items:
        raise ValueError("At least one purchase item is required.")

    # =====================================================
    # VALIDATE ALL ITEMS BEFORE STOCK MOVEMENT
    # =====================================================

    validated_items = []

    for item in items:

        validated_item = validate_purchase_item(item, retailer, branch)

        validated_items.append(validated_item)

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
    # PROCESS PURCHASE ITEMS
    # =====================================================

    for item in validated_items:

        product = item["product"]

        qty = item["qty"]
        free_qty = item["free_qty"]
        total_qty = item["total_qty"]

        batch_no = item["batch_no"]

        purchase_price = item["purchase_price"]
        sale_price = item["sale_price"]
        mrp = item["mrp"]

        expiry_date = item["expiry_date"]
        manufacture_date = item["manufacture_date"]

        # =====================================================
        # FIND OR CREATE STOCK BATCH
        # =====================================================

        batch, created = StockBatch.objects.select_for_update().get_or_create(
            retailer=retailer,
            branch=branch,
            product=product,
            batch_no=batch_no,
            defaults={
                "supplier": supplier,
                "quantity": total_qty,
                "available_qty": total_qty,
                "reserved_qty": 0,
                "purchase_price": purchase_price,
                "sale_price": sale_price,
                "mrp": mrp,
                "expiry_date": expiry_date,
                "manufacture_date": manufacture_date,
                "created_by": created_by,
            },
        )

        # =====================================================
        # UPDATE EXISTING BATCH
        # =====================================================

        if not created:

            if batch.expiry_date != expiry_date:
                raise ValueError(
                    f"Expiry date does not match existing batch " f"{batch_no}."
                )

            if batch.manufacture_date != manufacture_date:
                raise ValueError(
                    f"Manufacture date does not match existing batch " f"{batch_no}."
                )

            batch.quantity += total_qty
            batch.available_qty += total_qty

            batch.purchase_price = purchase_price
            batch.sale_price = sale_price
            batch.mrp = mrp

            batch.save(
                update_fields=[
                    "quantity",
                    "available_qty",
                    "purchase_price",
                    "sale_price",
                    "mrp",
                    "is_expired",
                    "updated_at",
                ]
            )

        # =====================================================
        # CALCULATE PURCHASE ITEM TOTAL
        # =====================================================

        item_total = Decimal(qty) * purchase_price

        total_amount += item_total

        # =====================================================
        # CREATE STOCK TRANSACTION ITEM
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
    # UPDATE PURCHASE TOTAL
    # =====================================================

    purchase.total_amount = total_amount

    purchase.save(
        update_fields=[
            "total_amount",
            "updated_at",
        ]
    )

    return purchase

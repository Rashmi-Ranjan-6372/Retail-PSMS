from decimal import Decimal, InvalidOperation

from django.db import transaction

from inventory.models.receipt_models import Receipt

from subscriptions.utils import (
    check_subscription_write_access,
    validate_branch_subscription,
)

# =====================================================
# UPDATE RECEIPT STATUS
# =====================================================


@transaction.atomic
def update_receipt_status(receipt):

    # =========================
    # LOCK RECEIPT
    # =========================

    try:
        receipt = Receipt.objects.select_for_update().get(id=receipt.id)
    except Receipt.DoesNotExist:
        raise ValueError("Receipt not found.")

    # =========================
    # SUBSCRIPTION VALIDATION
    # =========================

    check_subscription_write_access(receipt.retailer)

    validate_branch_subscription(receipt.retailer)

    # =========================
    # CONVERT AMOUNTS
    # =========================

    try:
        amount = Decimal(str(receipt.amount or 0))
        paid_amount = Decimal(str(receipt.paid_amount or 0))

    except (InvalidOperation, TypeError, ValueError):
        raise ValueError("Invalid receipt amount.")

    # =========================
    # VALIDATE AMOUNTS
    # =========================

    if amount <= 0:
        raise ValueError("Receipt amount must be greater than 0.")

    if paid_amount < 0:
        raise ValueError("Paid amount cannot be negative.")

    if paid_amount > amount:
        raise ValueError("Paid amount cannot exceed receipt amount.")

    # =========================
    # DUE CALCULATION
    # =========================

    receipt.due_amount = amount - paid_amount

    # =========================
    # STATUS CALCULATION
    # =========================

    if receipt.due_amount == 0:
        receipt.status = "RECEIVED"

    elif paid_amount > 0:
        receipt.status = "PARTIAL"

    else:
        receipt.status = "PENDING"

    # =========================
    # SAVE RECEIPT
    # =========================

    receipt.save(update_fields=["due_amount", "status", "updated_at"])

    return receipt

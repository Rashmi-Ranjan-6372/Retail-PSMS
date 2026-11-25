from decimal import Decimal, InvalidOperation

from django.db import transaction

from inventory.models.payment_models import Payment

from subscriptions.utils import (
    check_subscription_write_access,
    validate_branch_subscription,
)

# =====================================================
# UPDATE PAYMENT STATUS
# =====================================================


@transaction.atomic
def update_payment_status(payment):

    try:
        payment = Payment.objects.select_for_update().get(id=payment.id)
    except Payment.DoesNotExist:
        raise ValueError("Payment record not found.")

    check_subscription_write_access(payment.retailer)
    validate_branch_subscription(payment.retailer)

    # =========================
    # CONVERT AMOUNTS
    # =========================

    try:
        amount = Decimal(str(payment.amount or 0))
        paid_amount = Decimal(str(payment.paid_amount or 0))

    except (InvalidOperation, TypeError, ValueError):
        raise ValueError("Invalid payment amount.")

    # =========================
    # VALIDATE AMOUNTS
    # =========================

    if amount <= 0:
        raise ValueError("Payment amount must be greater than 0.")

    if paid_amount < 0:
        raise ValueError("Paid amount cannot be negative.")

    if paid_amount > amount:
        raise ValueError("Paid amount cannot exceed the total payment amount.")

    # =========================
    # DUE CALCULATION
    # =========================

    payment.due_amount = amount - paid_amount

    # =========================
    # STATUS CALCULATION
    # =========================

    if payment.due_amount == 0:
        payment.status = "PAID"

    elif paid_amount > 0:
        payment.status = "PARTIAL"

    else:
        payment.status = "PENDING"

    # =========================
    # SAVE PAYMENT
    # =========================

    payment.save(update_fields=["due_amount", "status", "updated_at"])

    return payment

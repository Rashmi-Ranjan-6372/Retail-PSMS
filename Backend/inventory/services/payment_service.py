
from decimal import Decimal, InvalidOperation

from django.db import transaction
from django.core.exceptions import ValidationError as DjangoValidationError

from inventory.models.payment_models import Payment


# =====================================================
# UPDATE PAYMENT STATUS
# =====================================================

@transaction.atomic
def update_payment_status(payment):

    try:

        payment = Payment.objects.select_for_update().get(
            pk=payment.pk
        )

    except Payment.DoesNotExist:

        raise ValueError("Payment record not found.")

    # =================================================
    # CONVERT AMOUNTS
    # =================================================

    try:

        amount = Decimal(str(payment.amount))
        paid_amount = Decimal(str(payment.paid_amount))

    except (InvalidOperation, TypeError, ValueError):

        raise ValueError("Invalid payment amount.")

    # =================================================
    # VALIDATE AMOUNTS
    # =================================================

    if amount <= 0:

        raise ValueError(
            "Payment amount must be greater than zero."
        )

    if paid_amount < 0:

        raise ValueError(
            "Paid amount cannot be negative."
        )

    if paid_amount > amount:

        raise ValueError(
            "Paid amount cannot exceed the total payment amount."
        )

    # =================================================
    # UPDATE PAYMENT
    # =================================================

    payment.amount = amount
    payment.paid_amount = paid_amount

    payment.calculate_payment()

    try:

        payment.save(
            update_fields=[
                "amount",
                "paid_amount",
                "due_amount",
                "status",
                "updated_at",
            ]
        )

    except DjangoValidationError as exc:

        raise ValueError(str(exc))

    return payment

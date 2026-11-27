from decimal import Decimal, InvalidOperation

from django.db import transaction
from django.core.exceptions import ValidationError as DjangoValidationError

from inventory.models.receipt_models import Receipt

# =====================================================
# UPDATE RECEIPT STATUS
# =====================================================


@transaction.atomic
def update_receipt_status(receipt):

    # =================================================
    # LOCK RECEIPT
    # =================================================

    try:

        receipt = Receipt.objects.select_for_update().get(pk=receipt.pk)

    except Receipt.DoesNotExist:

        raise ValueError("Receipt not found.")

    # =================================================
    # CONVERT AMOUNTS
    # =================================================

    try:

        amount = Decimal(str(receipt.amount))
        paid_amount = Decimal(str(receipt.paid_amount))

    except (InvalidOperation, TypeError, ValueError):

        raise ValueError("Invalid receipt amount.")

    # =================================================
    # VALIDATE AMOUNTS
    # =================================================

    if amount <= 0:

        raise ValueError("Receipt amount must be greater than zero.")

    if paid_amount < 0:

        raise ValueError("Paid amount cannot be negative.")

    if paid_amount > amount:

        raise ValueError("Paid amount cannot exceed receipt amount.")

    # =================================================
    # UPDATE RECEIPT
    # =================================================

    receipt.amount = amount
    receipt.paid_amount = paid_amount

    receipt.calculate_receipt()

    try:

        receipt.save(
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

    return receipt

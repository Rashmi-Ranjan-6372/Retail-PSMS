from django.db import transaction
from subscriptions.utils import (check_subscription_write_access, validate_branch_subscription)


# =====================================================
# PROCESS RECEIPT
# =====================================================

@transaction.atomic
def update_receipt_status(
    receipt
):

    check_subscription_write_access(
        receipt.retailer
    )

    validate_branch_subscription(
        receipt.retailer
    )

    # =========================
    # DUE CALCULATION
    # =========================

    receipt.due_amount = (
        (receipt.amount or 0) -
        (receipt.paid_amount or 0)
    )

    # =========================
    # STATUS CALCULATION
    # =========================

    if receipt.due_amount <= 0:
        receipt.status = "RECEIVED"

    elif receipt.paid_amount > 0:
        receipt.status = "PARTIAL"

    else:
        receipt.status = "PENDING"

    receipt.save(
        update_fields=[
            "due_amount",
            "status"
        ]
    )

    return receipt
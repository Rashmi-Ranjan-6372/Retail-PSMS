from django.db import transaction


# =====================================================
# PROCESS RECEIPT
# =====================================================

@transaction.atomic
def process_receipt(
    receipt
):

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

    receipt.save()
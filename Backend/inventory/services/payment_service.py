from django.db import transaction


# =====================================================
# PROCESS PAYMENT
# =====================================================

@transaction.atomic
def process_payment(
    payment
):

    # =========================
    # DUE CALCULATION
    # =========================

    payment.due_amount = (
        (payment.amount or 0) -
        (payment.paid_amount or 0)
    )

    # =========================
    # STATUS CALCULATION
    # =========================

    if payment.due_amount <= 0:

        payment.status = "PAID"

    elif payment.paid_amount > 0:

        payment.status = "PARTIAL"

    else:

        payment.status = "PENDING"

    payment.save()
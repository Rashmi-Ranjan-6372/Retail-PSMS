from django.db import transaction
from subscriptions.utils import (check_subscription_write_access,validate_branch_subscription)


# =====================================================
# UPDATE PAYMENT STATUS
# =====================================================

@transaction.atomic
def update_payment_status(payment):

    check_subscription_write_access(payment.retailer)
    validate_branch_subscription(payment.retailer)

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

    payment.save(
        update_fields=[
            "due_amount",
            "status"
        ]
    )

    return payment
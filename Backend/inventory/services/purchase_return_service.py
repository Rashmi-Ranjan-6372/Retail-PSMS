from decimal import Decimal
from django.db import transaction
from django.db.models import Sum
from inventory.models.purchase_return_item_models import (PurchaseReturnItem)
from subscriptions.utils import (check_subscription_write_access, validate_branch_subscription)


# =====================================================
# UPDATE PURCHASE RETURN TOTALS
# =====================================================

@transaction.atomic
def update_purchase_return_totals(purchase_return):

    check_subscription_write_access(
        purchase_return.retailer
    )

    validate_branch_subscription(
        purchase_return.retailer
    )

    # =====================================================
    # LOCK RETURN RECORD
    # =====================================================

    purchase_return = (
        purchase_return.__class__.objects
        .select_for_update()
        .get(id=purchase_return.id)
    )

    # =====================================================
    # GET TOTAL AMOUNT
    # =====================================================

    totals = (
        PurchaseReturnItem.objects.filter(
            purchase_return=purchase_return
        ).aggregate(
            total_amount=Sum("amount")
        )
    )

    total = Decimal(
        str(
            totals.get("total_amount") or 0
        )
    )

    # =====================================================
    # UPDATE TOTALS
    # =====================================================

    purchase_return.total_amount = total

    purchase_return.adjusted_amount = total

    # =====================================================
    # AUTO STATUS UPDATE
    # =====================================================

    if total > 0:

        purchase_return.status = "COMPLETED"

    else:

        purchase_return.status = "DRAFT"

    purchase_return.save(
        update_fields=[
            "total_amount",
            "adjusted_amount",
            "status",
        ]
    )

    return purchase_return
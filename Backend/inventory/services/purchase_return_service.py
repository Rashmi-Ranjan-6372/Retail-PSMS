from decimal import Decimal

from django.db import transaction
from django.db.models import Sum, DecimalField
from django.db.models.functions import Coalesce

from inventory.models.purchase_return_models import PurchaseReturn
from inventory.models.purchase_return_item_models import PurchaseReturnItem

from subscriptions.utils import (
    check_subscription_write_access,
    validate_branch_subscription,
)

# =====================================================
# UPDATE PURCHASE RETURN TOTALS
# =====================================================


@transaction.atomic
def update_purchase_return_totals(purchase_return):

    # =====================================================
    # LOCK RETURN RECORD
    # =====================================================

    try:
        purchase_return = PurchaseReturn.objects.select_for_update().get(
            id=purchase_return.id
        )
    except PurchaseReturn.DoesNotExist:
        raise ValueError("Purchase return not found.")

    # =====================================================
    # SUBSCRIPTION VALIDATION
    # =====================================================

    check_subscription_write_access(purchase_return.retailer)

    validate_branch_subscription(purchase_return.retailer)

    # =====================================================
    # GET TOTAL AMOUNT
    # =====================================================

    totals = PurchaseReturnItem.objects.filter(
        purchase_return=purchase_return
    ).aggregate(
        total_amount=Coalesce(
            Sum("amount"),
            Decimal("0.00"),
            output_field=DecimalField(max_digits=14, decimal_places=2),
        )
    )

    total = Decimal(str(totals["total_amount"]))

    # =====================================================
    # UPDATE TOTALS
    # =====================================================

    purchase_return.total_amount = total

    # Keep adjusted amount within the new return total.
    current_adjusted = Decimal(str(purchase_return.adjusted_amount or 0))

    purchase_return.adjusted_amount = min(current_adjusted, total)

    # =====================================================
    # SAVE TOTALS
    # =====================================================

    purchase_return.save(
        update_fields=["total_amount", "adjusted_amount", "updated_at"]
    )

    return purchase_return

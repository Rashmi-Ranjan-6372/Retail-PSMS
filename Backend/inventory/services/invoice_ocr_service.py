from inventory.models.sales_models import Sales
from inventory.models.receipt_models import Receipt

from subscriptions.utils import (
    check_subscription_write_access,
    validate_branch_subscription,
)


class InvoiceReceiptService:

    # =====================================================
    # GET SALES INVOICE
    # =====================================================

    @staticmethod
    def get_sales_invoice(invoice_no, user):

        retailer = getattr(user, "retailer", None)
        branch = getattr(user, "branch", None)

        if not retailer:
            raise ValueError("Retailer account is required.")

        check_subscription_write_access(retailer)
        validate_branch_subscription(retailer)

        sale = (
            Sales.objects.filter(
                invoice_no=invoice_no, retailer=retailer, branch=branch
            )
            .select_related("retailer", "branch", "customer")
            .first()
        )

        return sale

    # =====================================================
    # GET RECEIPT
    # =====================================================

    @staticmethod
    def get_receipt(receipt_no, user):

        retailer = getattr(user, "retailer", None)
        branch = getattr(user, "branch", None)

        if not retailer:
            raise ValueError("Retailer account is required.")

        check_subscription_write_access(retailer)
        validate_branch_subscription(retailer)

        receipt = (
            Receipt.objects.filter(
                receipt_no=receipt_no, retailer=retailer, branch=branch
            )
            .select_related("retailer", "branch", "customer")
            .first()
        )

        return receipt

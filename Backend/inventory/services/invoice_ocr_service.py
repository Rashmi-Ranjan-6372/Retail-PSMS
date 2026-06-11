from inventory.models.sales_models import Sales
from inventory.models.receipt_models import Receipt
from subscriptions.utils import (check_subscription_write_access, validate_branch_subscription)

class InvoiceReceiptService:

    @staticmethod
    def get_sales_invoice(invoice_no):

        sale = Sales.objects.filter(
            invoice_no=invoice_no
        ).select_related(
            "retailer"
        ).first()

        if sale:

            check_subscription_write_access(
                sale.retailer
            )

            validate_branch_subscription(
                sale.retailer
            )

        return sale

    @staticmethod
    def get_receipt(receipt_no):

        receipt = Receipt.objects.filter(
            receipt_no=receipt_no
        ).select_related(
            "retailer"
        ).first()

        if receipt:

            check_subscription_write_access(
                receipt.retailer
            )

            validate_branch_subscription(
                receipt.retailer
            )

        return receipt
from inventory.models.sales_models import Sales
from inventory.models.receipt_models import Receipt


class InvoiceReceiptService:

    @staticmethod
    def get_sales_invoice(invoice_no):

        return Sales.objects.filter(
            invoice_no=invoice_no
        ).first()

    @staticmethod
    def get_receipt(receipt_no):

        return Receipt.objects.filter(
            receipt_no=receipt_no
        ).first()
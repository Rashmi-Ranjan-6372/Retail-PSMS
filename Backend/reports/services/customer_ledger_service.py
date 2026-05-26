from inventory.models.sales_models import Sales


class CustomerLedgerService:

    @staticmethod
    def get_customer_ledger(customer_id):

        return Sales.objects.filter(
            customer_id=customer_id
        )
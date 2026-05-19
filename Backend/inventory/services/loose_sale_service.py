from inventory.models.sales_item_models import SalesItem


class LooseSaleService:

    @staticmethod
    def calculate_item_amount(
        qty,
        unit_price,
        discount=0,
        tax_percent=0
    ):

        base_amount = qty * unit_price

        discounted_amount = (
            base_amount - discount
        )

        tax_amount = (
            discounted_amount * tax_percent
        ) / 100

        final_amount = (
            discounted_amount + tax_amount
        )

        return {
            "base_amount": base_amount,
            "tax_amount": tax_amount,
            "final_amount": final_amount,
        }
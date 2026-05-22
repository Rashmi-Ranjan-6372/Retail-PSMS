from decimal import Decimal


# =====================================================
# CALCULATE STOCK VALUE
# =====================================================

def calculate_stock_value(
    quantity,
    price
):

    quantity = Decimal(quantity or 0)
    price = Decimal(price or 0)

    return quantity * price
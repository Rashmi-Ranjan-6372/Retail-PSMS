
from decimal import Decimal, InvalidOperation


# =====================================================
# CALCULATE STOCK VALUE
# =====================================================

def calculate_stock_value(quantity, price):

    try:
        quantity = Decimal(str(quantity or 0))
        price = Decimal(str(price or 0))

    except (InvalidOperation, ValueError, TypeError):
        raise ValueError("Quantity and price must be valid numeric values.")

    if not quantity.is_finite() or not price.is_finite():
        raise ValueError("Quantity and price must be finite numbers.")

    if quantity < 0:
        raise ValueError("Quantity cannot be negative.")

    if price < 0:
        raise ValueError("Price cannot be negative.")

    return quantity * price

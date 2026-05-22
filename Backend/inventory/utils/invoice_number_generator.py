from datetime import datetime


# =====================================================
# GENERATE INVOICE NUMBER
# =====================================================

def generate_invoice_number(last_id):

    year = datetime.now().year

    next_number = (last_id or 0) + 1

    return f"INV-{year}-{next_number:04d}"


# =====================================================
# GENERATE PAYMENT NUMBER
# =====================================================

def generate_payment_number(last_id):

    year = datetime.now().year

    next_number = (last_id or 0) + 1

    return f"PAY-{year}-{next_number:04d}"


# =====================================================
# GENERATE RECEIPT NUMBER
# =====================================================

def generate_receipt_number(last_id):

    year = datetime.now().year

    next_number = (last_id or 0) + 1

    return f"RCPT-{year}-{next_number:04d}"


# =====================================================
# GENERATE PURCHASE RETURN NUMBER
# =====================================================

def generate_purchase_return_number(last_id):

    year = datetime.now().year

    next_number = (last_id or 0) + 1

    return f"PR-{year}-{next_number:04d}"


# =====================================================
# GENERATE SALES RETURN NUMBER
# =====================================================

def generate_sales_return_number(last_id):

    year = datetime.now().year

    next_number = (last_id or 0) + 1

    return f"SR-{year}-{next_number:04d}"


# =====================================================
# GENERATE STOCK TRANSFER NUMBER
# =====================================================

def generate_transfer_number(last_id):

    year = datetime.now().year

    next_number = (last_id or 0) + 1

    return f"TR-{year}-{next_number:04d}"


# =====================================================
# GENERATE STOCK TRANSACTION NUMBER
# =====================================================

def generate_stock_transaction_number(last_id):

    year = datetime.now().year

    next_number = (last_id or 0) + 1

    return f"ST-{year}-{next_number:04d}"
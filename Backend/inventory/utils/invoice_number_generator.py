from django.utils import timezone

# =====================================================
# COMMON NUMBER GENERATOR
# =====================================================


def generate_document_number(prefix, last_id):

    year = timezone.localdate().year

    next_number = (last_id or 0) + 1

    return f"{prefix}-{year}-{next_number:04d}"


# =====================================================
# GENERATE INVOICE NUMBER
# =====================================================


def generate_invoice_number(last_id):

    return generate_document_number("INV", last_id)


# =====================================================
# GENERATE PAYMENT NUMBER
# =====================================================


def generate_payment_number(last_id):

    return generate_document_number("PAY", last_id)


# =====================================================
# GENERATE RECEIPT NUMBER
# =====================================================


def generate_receipt_number(last_id):

    return generate_document_number("RCPT", last_id)


# =====================================================
# GENERATE PURCHASE RETURN NUMBER
# =====================================================


def generate_purchase_return_number(last_id):

    return generate_document_number("PR", last_id)


# =====================================================
# GENERATE SALES RETURN NUMBER
# =====================================================


def generate_sales_return_number(last_id):

    return generate_document_number("SR", last_id)


# =====================================================
# GENERATE STOCK TRANSFER NUMBER
# =====================================================


def generate_transfer_number(last_id):

    return generate_document_number("TR", last_id)


# =====================================================
# GENERATE STOCK TRANSACTION NUMBER
# =====================================================


def generate_stock_transaction_number(last_id):

    return generate_document_number("ST", last_id)

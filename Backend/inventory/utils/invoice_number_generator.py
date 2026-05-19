from datetime import datetime


def generate_invoice_number(last_id):

    year = datetime.now().year

    return f"INV-{year}-{last_id + 1:04d}"
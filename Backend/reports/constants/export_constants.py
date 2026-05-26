# =========================
# EXPORT TYPES
# =========================

EXPORT_TYPES = (
    ("PDF", "PDF Export"),
    ("EXCEL", "Excel Export"),
    ("CSV", "CSV Export"),
)

# =========================
# FILE TYPES
# =========================

FILE_TYPES = (
    ("application/pdf", "PDF"),
    (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "Excel"
    ),
    ("text/csv", "CSV"),
)

# =========================
# EXPORT FILE NAMES
# =========================

EXPORT_FILE_NAMES = {
    "SALES": "sales_report",
    "PURCHASE": "purchase_report",
    "STOCK": "stock_report",
    "PROFIT_LOSS": "profit_loss_report",
    "SUPPLIER_LEDGER": "supplier_ledger",
    "CUSTOMER_LEDGER": "customer_ledger",
}
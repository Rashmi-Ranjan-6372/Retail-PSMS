# =========================
# REPORT TYPES
# =========================

REPORT_TYPES = (
    ("SALES", "Sales Report"),
    ("PURCHASE", "Purchase Report"),
    ("SALES_RETURN", "Sales Return Report"),
    ("PURCHASE_RETURN", "Purchase Return Report"),
    ("STOCK", "Stock Report"),
    ("EXPIRY", "Expiry Report"),
    ("LOW_STOCK", "Low Stock Report"),
    ("PRODUCT_LEDGER", "Product Ledger"),
    ("SUPPLIER_LEDGER", "Supplier Ledger"),
    ("CUSTOMER_LEDGER", "Customer Ledger"),
    ("PROFIT_LOSS", "Profit & Loss"),
)

# =========================
# REPORT STATUS
# =========================

REPORT_STATUS = (
    ("ACTIVE", "Active"),
    ("INACTIVE", "Inactive"),
)

# =========================
# DATE FILTERS
# =========================

DATE_FILTERS = (
    ("TODAY", "Today"),
    ("WEEK", "This Week"),
    ("MONTH", "This Month"),
    ("YEAR", "This Year"),
    ("CUSTOM", "Custom Range"),
)

# =========================
# STOCK FILTERS
# =========================

STOCK_FILTERS = (
    ("ALL", "All Stock"),
    ("LOW_STOCK", "Low Stock"),
    ("OUT_OF_STOCK", "Out Of Stock"),
    ("EXPIRED", "Expired Stock"),
)

# =========================
# LEDGER TYPES
# =========================

LEDGER_TYPES = (
    ("SUPPLIER", "Supplier Ledger"),
    ("CUSTOMER", "Customer Ledger"),
    ("PRODUCT", "Product Ledger"),
)

# =========================
# DASHBOARD CARDS
# =========================

DASHBOARD_CARDS = (
    ("TOTAL_SALES", "Total Sales"),
    ("TOTAL_PURCHASE", "Total Purchase"),
    ("TOTAL_CUSTOMERS", "Total Customers"),
    ("TOTAL_SUPPLIERS", "Total Suppliers"),
    ("TOTAL_PRODUCTS", "Total Products"),
    ("LOW_STOCK", "Low Stock Items"),
    ("EXPIRED_PRODUCTS", "Expired Products"),
    ("TOTAL_PROFIT", "Total Profit"),
)


# =========================
# DASHBOARD CHART TYPES
# =========================

CHART_TYPES = (
    ("BAR", "Bar Chart"),
    ("LINE", "Line Chart"),
    ("PIE", "Pie Chart"),
    ("DOUGHNUT", "Doughnut Chart"),
)


# =========================
# ANALYTICS TYPES
# =========================

ANALYTICS_TYPES = (
    ("SALES_ANALYTICS", "Sales Analytics"),
    ("PURCHASE_ANALYTICS", "Purchase Analytics"),
    ("STOCK_ANALYTICS", "Stock Analytics"),
    ("PROFIT_ANALYTICS", "Profit Analytics"),
)


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
        "Excel",
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

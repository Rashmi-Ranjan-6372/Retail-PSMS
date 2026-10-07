# =========================
# TRANSACTION TYPES
# =========================

TRANSACTION_TYPE = (
    ("OPENING", "Opening Stock"),
    ("PURCHASE", "Purchase Entry"),
    ("PURCHASE_RETURN", "Purchase Return"),
    ("SALE", "Sales Billing"),
    ("SALES_RETURN", "Sales Return"),
    ("ADJUSTMENT_PLUS", "Stock Adjustment +"),
    ("ADJUSTMENT_MINUS", "Stock Adjustment -"),
    ("EXPIRY", "Expiry Damage"),
    ("DAMAGE", "Damage Stock"),
    ("TRANSFER_IN", "Stock Transfer In"),
    ("TRANSFER_OUT", "Stock Transfer Out"),
)


# =========================
# SALE TYPE
# =========================

SALE_TYPE = (
    ("STRIP", "Strip Sale"),
    ("LOOSE", "Loose Sale"),
)


# =========================
# SALE STATUS
# =========================

SALE_STATUS = (
    ("DRAFT", "Draft"),
    ("COMPLETED", "Completed"),
    ("CANCELLED", "Cancelled"),
)


# =========================
# PURCHASE STATUS
# =========================

PURCHASE_STATUS = (
    ("DRAFT", "Draft"),
    ("RECEIVED", "Received"),
    ("PARTIAL", "Partially Received"),
    ("COMPLETED", "Completed"),
    ("CANCELLED", "Cancelled"),
)


# =========================
# PAYMENT STATUS
# =========================

PAYMENT_STATUS = (
    ("PAID", "Paid"),
    ("PARTIAL", "Partial Paid"),
    ("UNPAID", "Unpaid"),
)


# =========================
# STOCK STATUS
# =========================

STOCK_STATUS = (
    ("IN_STOCK", "In Stock"),
    ("LOW_STOCK", "Low Stock"),
    ("OUT_OF_STOCK", "Out of Stock"),
)


# =========================
# EXPIRY STATUS
# =========================

EXPIRY_STATUS = (
    ("VALID", "Valid"),
    ("NEAR_EXPIRY", "Near Expiry"),
    ("EXPIRED", "Expired"),
)


# =========================
# BATCH STATUS
# =========================

BATCH_STATUS = (
    ("ACTIVE", "Active"),
    ("EXPIRED", "Expired"),
    ("DAMAGED", "Damaged"),
    ("BLOCKED", "Blocked"),
)


# =========================
# PAYMENT METHOD
# =========================

PAYMENT_METHOD = (
    ("CASH", "Cash"),
    ("UPI", "UPI"),
    ("CARD", "Card"),
    ("BANK_TRANSFER", "Bank Transfer"),
)


# =========================
# INVOICE PREFIX
# =========================

INVOICE_PREFIX = {
    "SALE": "SAL",
    "PURCHASE": "PUR",
    "PURCHASE_RETURN": "PR",
    "SALES_RETURN": "SR",
    "PAYMENT": "PAY",
    "RECEIPT": "REC",
}


# =========================
# RETURN TYPE
# =========================

RETURN_TYPE = (
    ("CUSTOMER", "Customer Return"),
    ("SUPPLIER", "Supplier Return"),
)


# =========================
# RETURN CONDITION
# =========================

RETURN_CONDITION = (
    ("GOOD", "Good Stock"),
    ("DAMAGED", "Damaged"),
)


# =========================
# RETURN STATUS
# =========================

RETURN_STATUS = (
    ("DRAFT", "Draft"),
    ("COMPLETED", "Completed"),
    ("CANCELLED", "Cancelled"),
)


# =========================
# SALES RETURN STATUS
# =========================

SALES_RETURN_STATUS = (
    ("DRAFT", "Draft"),
    ("COMPLETED", "Completed"),
    ("CANCELLED", "Cancelled"),
)


# =========================
# ADJUSTMENT REASONS
# =========================

ADJUSTMENT_REASON = (
    ("MANUAL_CORRECTION", "Manual Correction"),
    ("STOCK_COUNT_MISMATCH", "Stock Count Mismatch"),
    ("SYSTEM_ERROR", "System Error"),
)


# =========================
# ADJUSTMENT TYPE
# =========================

ADJUSTMENT_TYPE = (
    ("IN", "Stock In"),
    ("OUT", "Stock Out"),
)


# =========================
# ADJUSTMENT STATUS
# =========================

ADJUSTMENT_STATUS = (
    ("DRAFT", "Draft"),
    ("POSTED", "Posted"),
    ("CANCELLED", "Cancelled"),
)


# =========================
# DAMAGE / EXPIRY REASON
# =========================

STOCK_ISSUE_REASON = (
    ("EXPIRY", "Expired Stock"),
    ("DAMAGE", "Damaged Stock"),
)


# =========================
# RECEIPT STATUS
# =========================

RECEIPT_STATUS = (
    ("RECEIVED", "Received"),
    ("PARTIAL", "Partial"),
    ("PENDING", "Pending"),
)


# =========================
# STOCK TRANSACTION STATUS
# =========================

STOCK_TRANSACTION_STATUS = (
    ("DRAFT", "Draft"),
    ("POSTED", "Posted"),
    ("CANCELLED", "Cancelled"),
)


# =========================
# TRANSFER STATUS
# =========================

TRANSFER_STATUS = (
    ("PENDING", "Pending"),
    ("RECEIVED", "Received"),
    ("CANCELLED", "Cancelled"),
)

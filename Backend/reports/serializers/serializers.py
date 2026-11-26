from rest_framework import serializers

# =========================
# COMMON FIELD CONFIGURATION
# =========================

MONEY_MAX_DIGITS = 15
MONEY_DECIMAL_PLACES = 2

QUANTITY_MAX_DIGITS = 15
QUANTITY_DECIMAL_PLACES = 3


# =========================
# ANALYTICS SERIALIZER
# =========================


class AnalyticsSerializer(serializers.Serializer):

    total_sales = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    total_purchase = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    total_profit = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    total_customers = serializers.IntegerField()

    total_suppliers = serializers.IntegerField()


# =========================
# CUSTOMER LEDGER SERIALIZER
# =========================


class CustomerLedgerSerializer(serializers.Serializer):

    customer = serializers.CharField()

    invoice_no = serializers.CharField()

    total_amount = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    paid_amount = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    due_amount = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    created_at = serializers.DateTimeField()


# =========================
# DASHBOARD SERIALIZER
# =========================


class DashboardSerializer(serializers.Serializer):

    total_sales = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    total_purchase = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    total_profit = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    total_stock = serializers.DecimalField(
        max_digits=QUANTITY_MAX_DIGITS,
        decimal_places=QUANTITY_DECIMAL_PLACES,
    )


# =========================
# EXPIRY REPORT SERIALIZER
# =========================


class ExpiryReportSerializer(serializers.Serializer):

    product = serializers.CharField()

    batch_no = serializers.CharField()

    branch = serializers.CharField()

    expiry_date = serializers.DateField()

    available_qty = serializers.DecimalField(
        max_digits=QUANTITY_MAX_DIGITS,
        decimal_places=QUANTITY_DECIMAL_PLACES,
    )

    is_expired = serializers.BooleanField()


# =========================
# LOW STOCK REPORT SERIALIZER
# =========================


class LowStockReportSerializer(serializers.Serializer):

    product = serializers.CharField()

    batch_no = serializers.CharField()

    branch = serializers.CharField()

    available_qty = serializers.DecimalField(
        max_digits=QUANTITY_MAX_DIGITS,
        decimal_places=QUANTITY_DECIMAL_PLACES,
    )


# =========================
# PRODUCT LEDGER SERIALIZER
# =========================

class ProductLedgerSerializer(serializers.Serializer):

    transaction_no = serializers.CharField()

    transaction_type = serializers.CharField()

    product = serializers.CharField()

    qty = serializers.DecimalField(
        max_digits=QUANTITY_MAX_DIGITS,
        decimal_places=QUANTITY_DECIMAL_PLACES,
    )

    total_amount = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    created_at = serializers.DateTimeField()


# =========================
# PROFIT & LOSS SERIALIZER
# =========================


class ProfitLossSerializer(serializers.Serializer):

    branch = serializers.CharField()

    sales = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    purchase = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    profit = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )


# =========================
# PURCHASE REPORT SERIALIZER
# =========================


class PurchaseReportSerializer(serializers.Serializer):

    transaction_no = serializers.CharField()

    supplier = serializers.CharField()

    branch = serializers.CharField()

    total_amount = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    status = serializers.CharField()

    created_at = serializers.DateTimeField()


# =========================
# PURCHASE RETURN REPORT SERIALIZER
# =========================


class PurchaseReturnReportSerializer(serializers.Serializer):

    return_no = serializers.CharField()

    supplier = serializers.CharField()

    branch = serializers.CharField()

    total_amount = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    adjusted_amount = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    status = serializers.CharField()

    created_at = serializers.DateTimeField()


# =========================
# SALES REPORT SERIALIZER
# =========================


class SalesReportSerializer(serializers.Serializer):

    invoice_no = serializers.CharField()

    customer = serializers.CharField()

    branch = serializers.CharField()

    total_amount = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    discount = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    net_amount = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    paid_amount = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    due_amount = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    payment_status = serializers.CharField()

    created_at = serializers.DateTimeField()


# =========================
# SALES RETURN REPORT SERIALIZER
# =========================


class SalesReturnReportSerializer(serializers.Serializer):

    return_no = serializers.CharField()

    sales_invoice = serializers.CharField()

    branch = serializers.CharField()

    total_amount = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    refund_amount = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    status = serializers.CharField()

    created_at = serializers.DateTimeField()


# =========================
# STOCK REPORT SERIALIZER
# =========================


class StockReportSerializer(serializers.Serializer):

    product = serializers.CharField()

    batch_no = serializers.CharField()

    branch = serializers.CharField()

    quantity = serializers.DecimalField(
        max_digits=QUANTITY_MAX_DIGITS,
        decimal_places=QUANTITY_DECIMAL_PLACES,
    )

    available_qty = serializers.DecimalField(
        max_digits=QUANTITY_MAX_DIGITS,
        decimal_places=QUANTITY_DECIMAL_PLACES,
    )

    reserved_qty = serializers.DecimalField(
        max_digits=QUANTITY_MAX_DIGITS,
        decimal_places=QUANTITY_DECIMAL_PLACES,
    )

    purchase_price = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    sale_price = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    expiry_date = serializers.DateField()


# =========================
# SUPPLIER LEDGER SERIALIZER
# =========================

class SupplierLedgerSerializer(serializers.Serializer):

    supplier = serializers.CharField()

    transaction_no = serializers.CharField()

    total_amount = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    created_at = serializers.DateTimeField()
from rest_framework import serializers

# =====================================================
# COMMON FIELD CONFIGURATION
# =====================================================

MONEY_MAX_DIGITS = 15
MONEY_DECIMAL_PLACES = 2

QUANTITY_MAX_DIGITS = 15
QUANTITY_DECIMAL_PLACES = 3


# =====================================================
# COMMON SERIALIZER
# =====================================================


class ReportSerializer(serializers.Serializer):
    pass


class ReportSummarySerializer(ReportSerializer):

    summary = serializers.DictField(
        child=serializers.JSONField(),
        required=False,
    )

    data = serializers.ListField(
        child=serializers.DictField(
            child=serializers.JSONField(),
        ),
        required=False,
    )


# =====================================================
# ANALYTICS SERIALIZER
# =====================================================


class AnalyticsSerializer(ReportSerializer):

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
        allow_null=True,
    )

    total_customers = serializers.IntegerField()

    total_suppliers = serializers.IntegerField()


# =====================================================
# CUSTOMER LEDGER SERIALIZER
# =====================================================


class CustomerLedgerSerializer(ReportSerializer):

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


# =====================================================
# DASHBOARD SERIALIZER
# Matches DashboardService.get_dashboard()
# =====================================================


class DashboardSerializer(ReportSerializer):

    total_sales = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    invoice_count = serializers.IntegerField()

    total_stock = serializers.DecimalField(
        max_digits=QUANTITY_MAX_DIGITS,
        decimal_places=QUANTITY_DECIMAL_PLACES,
    )


# =====================================================
# EXPIRY REPORT SERIALIZER
# =====================================================


class ExpiryReportSerializer(ReportSerializer):

    product = serializers.CharField()

    batch_no = serializers.CharField()

    branch = serializers.CharField(
        allow_null=True,
    )

    expiry_date = serializers.DateField(
        allow_null=True,
    )

    available_qty = serializers.DecimalField(
        max_digits=QUANTITY_MAX_DIGITS,
        decimal_places=QUANTITY_DECIMAL_PLACES,
    )

    is_expired = serializers.BooleanField()


# =====================================================
# LOW STOCK REPORT SERIALIZER
# =====================================================


class LowStockReportSerializer(ReportSerializer):

    product = serializers.CharField()

    batch_no = serializers.CharField()

    branch = serializers.CharField(
        allow_null=True,
    )

    available_qty = serializers.DecimalField(
        max_digits=QUANTITY_MAX_DIGITS,
        decimal_places=QUANTITY_DECIMAL_PLACES,
    )


# =====================================================
# PRODUCT LEDGER SERIALIZER
# =====================================================


class ProductLedgerSerializer(ReportSerializer):

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


# =====================================================
# PROFIT AND LOSS SERIALIZER
# Matches ProfitLossService.get_report()
# =====================================================


class ProfitLossOverallSerializer(ReportSerializer):

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
        allow_null=True,
    )


class ProfitLossSerializer(ReportSerializer):

    overall = ProfitLossOverallSerializer()

    branch_wise = serializers.ListField(
        child=serializers.DictField(
            child=serializers.JSONField(),
        ),
    )

    message = serializers.CharField(
        allow_blank=True,
        required=False,
    )


# =====================================================
# PURCHASE REPORT SERIALIZER
# =====================================================


class PurchaseReportSerializer(ReportSerializer):

    transaction_no = serializers.CharField()

    supplier = serializers.CharField()

    branch = serializers.CharField(
        allow_null=True,
    )

    total_amount = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    status = serializers.CharField()

    created_at = serializers.DateTimeField()


class PurchaseReportSummarySerializer(ReportSerializer):

    total_purchase = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    purchase_count = serializers.IntegerField()


class PurchaseReportResponseSerializer(ReportSerializer):

    summary = PurchaseReportSummarySerializer()

    data = PurchaseReportSerializer(
        many=True,
    )


# =====================================================
# PURCHASE RETURN REPORT SERIALIZER
# =====================================================


class PurchaseReturnReportSerializer(ReportSerializer):

    return_no = serializers.CharField()

    supplier = serializers.CharField()

    branch = serializers.CharField(
        allow_null=True,
    )

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


class PurchaseReturnSummarySerializer(ReportSerializer):

    total_returns = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    return_count = serializers.IntegerField()


class PurchaseReturnReportResponseSerializer(ReportSerializer):

    summary = PurchaseReturnSummarySerializer()

    data = PurchaseReturnReportSerializer(
        many=True,
    )


# =====================================================
# SALES REPORT SERIALIZER
# =====================================================


class SalesReportSerializer(ReportSerializer):

    invoice_no = serializers.CharField()

    customer = serializers.CharField()

    branch = serializers.CharField(
        allow_null=True,
    )

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


class SalesReportSummarySerializer(ReportSerializer):

    total_sales = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    total_paid = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    total_due = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    invoice_count = serializers.IntegerField()


class SalesReportResponseSerializer(ReportSerializer):

    summary = SalesReportSummarySerializer()

    data = SalesReportSerializer(
        many=True,
    )


# =====================================================
# SALES RETURN REPORT SERIALIZER
# =====================================================


class SalesReturnReportSerializer(ReportSerializer):

    return_no = serializers.CharField()

    sales_invoice = serializers.CharField(
        source="sales.invoice_no",
    )

    branch = serializers.CharField(
        allow_null=True,
    )

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


class SalesReturnSummarySerializer(ReportSerializer):

    total_returns = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    refund_amount = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    return_count = serializers.IntegerField()


class SalesReturnReportResponseSerializer(ReportSerializer):

    summary = SalesReturnSummarySerializer()

    data = SalesReturnReportSerializer(
        many=True,
    )


# =====================================================
# STOCK REPORT SERIALIZER
# =====================================================


class StockReportSerializer(ReportSerializer):

    product = serializers.CharField()

    batch_no = serializers.CharField()

    branch = serializers.CharField(
        allow_null=True,
    )

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

    expiry_date = serializers.DateField(
        allow_null=True,
    )


class StockReportSummarySerializer(ReportSerializer):

    total_stock = serializers.DecimalField(
        max_digits=QUANTITY_MAX_DIGITS,
        decimal_places=QUANTITY_DECIMAL_PLACES,
    )

    batch_count = serializers.IntegerField()


class StockReportResponseSerializer(ReportSerializer):

    summary = StockReportSummarySerializer()

    data = StockReportSerializer(
        many=True,
    )


# =====================================================
# SUPPLIER LEDGER SERIALIZER
# =====================================================


class SupplierLedgerSerializer(ReportSerializer):

    supplier = serializers.CharField()

    transaction_no = serializers.CharField()

    total_amount = serializers.DecimalField(
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=MONEY_DECIMAL_PLACES,
    )

    created_at = serializers.DateTimeField()

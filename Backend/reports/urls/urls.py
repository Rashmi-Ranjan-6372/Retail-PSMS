
from django.urls import path

from reports.views import (
    AnalyticsView,
    CustomerLedgerView,
    DashboardView,
    ExpiryReportView,
    GSTReportView,
    LowStockReportView,
    PaymentReportView,
    ProductLedgerView,
    ProfitLossView,
    PurchaseReportView,
    PurchaseReturnReportView,
    ReceiptReportView,
    SalesReportView,
    SalesReturnReportView,
    StockAdjustmentReportView,
    StockReportView,
    StockTransferReportView,
    SupplierLedgerView,
)


urlpatterns = [
    path("analytics/",AnalyticsView.as_view(),name="analytics-report"),
    path("customer-ledger/",CustomerLedgerView.as_view(),name="customer-ledger-report"),
    path("dashboard/",DashboardView.as_view(),name="dashboard-report"),
    path("expiry/",ExpiryReportView.as_view(),name="expiry-report"),
    path("gst/",GSTReportView.as_view(),name="gst-report"),
    path("low-stock/",LowStockReportView.as_view(),name="low-stock-report"),
    path("payment/",PaymentReportView.as_view(),name="payment-report"),
    path("product-ledger/",ProductLedgerView.as_view(),name="product-ledger-report"),
    path("profit-loss/",ProfitLossView.as_view(),name="profit-loss-report"),
    path("purchase/",PurchaseReportView.as_view(),name="purchase-report"),
    path("purchase-return/",PurchaseReturnReportView.as_view(),name="purchase-return-report"),
    path("receipt/",ReceiptReportView.as_view(),name="receipt-report"),
    path("sales/",SalesReportView.as_view(),name="sales-report"),
    path("sales-return/",SalesReturnReportView.as_view(),name="sales-return-report"),
    path("stock-adjustment/",StockAdjustmentReportView.as_view(),name="stock-adjustment-report"),
    path("stock/",StockReportView.as_view(),name="stock-report"),
    path("stock-transfer/",StockTransferReportView.as_view(),name="stock-transfer-report"),
    path("supplier-ledger/",SupplierLedgerView.as_view(),name="supplier-ledger-report"),
]

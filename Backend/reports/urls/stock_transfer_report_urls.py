from django.urls import path
from reports.views.stock_transfer_report_view import StockTransferReportView

urlpatterns = [
    path("stock-transfer/", StockTransferReportView.as_view(), name="stock-transfer-report"),
]
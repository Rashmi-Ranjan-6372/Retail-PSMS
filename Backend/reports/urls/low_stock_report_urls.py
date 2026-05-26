from django.urls import path
from reports.views.low_stock_report_view import LowStockReportView

urlpatterns = [
    path("low-stock/", LowStockReportView.as_view(), name="low-stock-report"),
]
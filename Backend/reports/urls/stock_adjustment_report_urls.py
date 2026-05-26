from django.urls import path
from reports.views.stock_adjustment_report_view import StockAdjustmentReportView

urlpatterns = [
    path("stock-adjustment/", StockAdjustmentReportView.as_view(), name="stock-adjustment-report"),
]
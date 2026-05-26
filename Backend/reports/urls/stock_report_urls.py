from django.urls import path
from reports.views.stock_report_view import StockReportView

urlpatterns = [
    path("stock/", StockReportView.as_view(), name="stock-report"),
]
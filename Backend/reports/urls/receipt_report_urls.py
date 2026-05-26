from django.urls import path
from reports.views.receipt_report_view import ReceiptReportView

urlpatterns = [
    path("receipt/", ReceiptReportView.as_view(), name="receipt-report"),
]
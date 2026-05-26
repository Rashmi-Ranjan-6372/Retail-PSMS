from django.urls import path
from reports.views.payment_report_view import PaymentReportView

urlpatterns = [
    path("payment/", PaymentReportView.as_view(), name="payment-report"),
]
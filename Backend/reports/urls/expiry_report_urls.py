from django.urls import path
from reports.views.expiry_report_view import ExpiryReportView

urlpatterns = [
    path("expiry/", ExpiryReportView.as_view(), name="expiry-report"),
]
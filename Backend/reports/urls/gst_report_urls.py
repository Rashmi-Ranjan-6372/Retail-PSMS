from django.urls import path
from reports.views.gst_report_view import GSTReportView

urlpatterns = [
    path("gst/", GSTReportView.as_view(), name="gst-report"),
]
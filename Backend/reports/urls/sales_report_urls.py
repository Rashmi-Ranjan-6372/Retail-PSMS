from django.urls import path
from reports.views.sales_report_view import SalesReportView

urlpatterns = [
    path("sales/", SalesReportView.as_view(), name="sales-report"),
]
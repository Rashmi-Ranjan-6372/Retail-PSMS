from django.urls import path
from reports.views.sales_return_report_view import SalesReturnReportView

urlpatterns = [
    path("sales-return/", SalesReturnReportView.as_view(), name="sales-return-report"),
]
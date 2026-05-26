from django.urls import path
from reports.views.purchase_report_view import PurchaseReportView

urlpatterns = [
    path("purchase/", PurchaseReportView.as_view(), name="purchase-report"),
]
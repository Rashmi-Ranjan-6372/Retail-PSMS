from django.urls import path
from reports.views.purchase_return_report_view import PurchaseReturnReportView

urlpatterns = [
    path("purchase-return/", PurchaseReturnReportView.as_view(), name="purchase-return-report"),
]
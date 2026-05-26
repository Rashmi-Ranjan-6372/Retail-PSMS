from django.urls import path
from reports.views.customer_ledger_view import CustomerLedgerView

urlpatterns = [
    path("customer-ledger/", CustomerLedgerView.as_view(), name="customer-ledger-report"),
]
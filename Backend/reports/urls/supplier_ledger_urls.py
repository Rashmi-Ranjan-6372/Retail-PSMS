from django.urls import path
from reports.views.supplier_ledger_view import SupplierLedgerView

urlpatterns = [
    path("supplier-ledger/", SupplierLedgerView.as_view(), name="supplier-ledger-report"),
]
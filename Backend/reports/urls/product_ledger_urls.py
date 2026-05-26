from django.urls import path
from reports.views.product_ledger_view import ProductLedgerView

urlpatterns = [
    path("product-ledger/", ProductLedgerView.as_view(), name="product-ledger-report"),
]
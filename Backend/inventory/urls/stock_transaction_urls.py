from django.urls import path

from inventory.views.stock_transaction_views import (
    StockTransactionListCreateView,
    StockTransactionDetailView,
)

urlpatterns = [

    path(
        "stock-transactions/",
        StockTransactionListCreateView.as_view(),
        name="stock-transaction-list-create",
    ),

    path(
        "stock-transactions/<int:pk>/",
        StockTransactionDetailView.as_view(),
        name="stock-transaction-detail",
    ),
]
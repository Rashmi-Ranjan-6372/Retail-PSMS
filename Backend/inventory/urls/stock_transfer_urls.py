from django.urls import path

from inventory.views.stock_transfer_views import (
    StockTransferListCreateView,
    StockTransferDetailView,
)

urlpatterns = [

    # =================================================
    # STOCK TRANSFER
    # =================================================

    path(
        "",
        StockTransferListCreateView.as_view(),
        name="stock-transfer-list-create"
    ),

    path(
        "<int:pk>/",
        StockTransferDetailView.as_view(),
        name="stock-transfer-detail"
    ),
]
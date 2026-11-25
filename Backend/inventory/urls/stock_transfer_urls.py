from django.urls import path

from inventory.views.stock_transfer_views import (
    StockTransferListCreateView,
    StockTransferDetailView,
)

urlpatterns = [
    path("stock-transfer/",StockTransferListCreateView.as_view(),name="stock-transfer-list-create"),
    path("stock-transfer/<int:pk>/",StockTransferDetailView.as_view(),name="stock-transfer-detail"),
]
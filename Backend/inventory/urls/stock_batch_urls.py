from django.urls import path

from inventory.views.stock_batch_views import (
    StockBatchListCreateView,
    StockBatchDetailView,
)

urlpatterns = [
    path("stock-batches/", StockBatchListCreateView.as_view(), name="stock-batch-list-create",),
    path("stock-batches/<int:pk>/", StockBatchDetailView.as_view(), name="stock-batch-detail",),
]
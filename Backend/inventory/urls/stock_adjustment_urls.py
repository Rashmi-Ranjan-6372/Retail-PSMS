from django.urls import path

from inventory.views.stock_adjustment_views import (
    StockAdjustmentListCreateView,
    StockAdjustmentDetailView,
)

urlpatterns = [

    # ================= STOCK ADJUSTMENT ================= #

    path(
        "stock-adjustments/",
        StockAdjustmentListCreateView.as_view(),
        name="stock-adjustment-list-create"
    ),

    path(
        "stock-adjustments/<int:pk>/",
        StockAdjustmentDetailView.as_view(),
        name="stock-adjustment-detail"
    ),
]
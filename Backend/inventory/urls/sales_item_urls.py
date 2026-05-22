# inventory/urls/sales_item_urls.py

from django.urls import path

from inventory.views.sales_item_views import (
    SalesItemListCreateView,
    SalesItemDetailView,
)

urlpatterns = [

    # ==========================================
    # SALES ITEM LIST + CREATE
    # ==========================================
    path(
        "",
        SalesItemListCreateView.as_view(),
        name="sales-item-list-create",
    ),

    # ==========================================
    # SALES ITEM DETAIL
    # ==========================================

    path(
        "<int:pk>/",
        SalesItemDetailView.as_view(),
        name="sales-item-detail",
    ),

]
# inventory/urls/sales_item_urls.py

from django.urls import path

from inventory.views.sales_item_views import (
    SalesItemListCreateView,
    SalesItemDetailView,
)

urlpatterns = [
    path("sales-items/",SalesItemListCreateView.as_view(),name="sales-item-list-create",),
    path("sales-items/<int:pk>/",SalesItemDetailView.as_view(),name="sales-item-detail",),
]
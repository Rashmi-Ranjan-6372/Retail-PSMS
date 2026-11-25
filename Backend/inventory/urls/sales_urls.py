from django.urls import path

from inventory.views.sales_views import (
    SalesListCreateView,
    SalesDetailView,
)

urlpatterns = [
    path("sales/", SalesListCreateView.as_view(), name="sales-list-create",),
    path("sales/<int:pk>/", SalesDetailView.as_view(), name="sales-detail",),
]
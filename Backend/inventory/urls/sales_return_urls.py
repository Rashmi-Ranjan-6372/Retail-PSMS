from django.urls import path

from inventory.views.sales_return_views import (
    SalesReturnListCreateView,
    SalesReturnDetailView,
)

urlpatterns = [
    path("sales-return/",SalesReturnListCreateView.as_view(),name="sales-return-list-create",),
    path("sales-return/<int:pk>/",SalesReturnDetailView.as_view(),name="sales-return-detail",),
]
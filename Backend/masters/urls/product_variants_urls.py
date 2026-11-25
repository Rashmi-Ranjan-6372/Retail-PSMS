
from django.urls import path

from masters.views.product_variants_views import (
    ProductVariantListCreateView,
    ProductVariantDetailView,
)

urlpatterns = [
    path("product-variant/",ProductVariantListCreateView.as_view(),name="product-variant-list-create"),
    path("product-variant/<int:pk>/",ProductVariantDetailView.as_view(),name="product-variant-detail"),
]

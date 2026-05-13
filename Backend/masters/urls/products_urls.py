from django.urls import path
from masters.views.products_views import *

urlpatterns = [
    path("products/create/", ProductCreateView.as_view(), name="product-create"),
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("products/update/<int:pk>/", ProductUpdateView.as_view(), name="product-update"),
    path("products/deactivate/<int:pk>/", ProductSoftDeleteView.as_view(), name="product-soft-delete"),
    path("products/delete/<int:pk>/", ProductDeleteView.as_view(), name="product-delete"),
]
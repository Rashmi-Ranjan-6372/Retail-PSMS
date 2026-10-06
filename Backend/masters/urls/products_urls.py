from django.urls import path
from masters.views.products_views import *

urlpatterns = [
    path("products/create/", ProductCreateAPIView.as_view(), name="product-create"),
    path("products/", ProductListAPIView.as_view(), name="product-list"),
    path("products/<int:pk>/", ProductDetailAPIView.as_view(), name="product-detail"),
    path("products/update/<int:pk>/", ProductUpdateAPIView.as_view(), name="product-update"),
    path("products/deactivate/<int:pk>/", ProductSoftDeleteAPIView.as_view(), name="product-soft-delete"),
    path("products/delete/<int:pk>/", ProductDeleteAPIView.as_view(), name="product-delete"),
]
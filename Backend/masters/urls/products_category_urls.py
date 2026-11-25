from django.urls import path

from masters.views.products_category_views import (
    ProductCategoryListCreateAPIView,
    ProductCategoryDetailAPIView,
    ProductCategoryDeactivateAPIView,
    ProductCategoryRestoreAPIView,
)

urlpatterns = [
    path("products-categories/", ProductCategoryListCreateAPIView.as_view(), name="product-category-list-create",),
    path("products-categories/<int:pk>/", ProductCategoryDetailAPIView.as_view(), name="product-category-detail",),
    path("products-categories/deactivate/<int:pk>/", ProductCategoryDeactivateAPIView.as_view(), name="product-category-deactivate",),
    path("products-categories/restore/<int:pk>/", ProductCategoryRestoreAPIView.as_view(), name="product-category-restore",),
]

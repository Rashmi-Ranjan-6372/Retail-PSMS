from django.urls import path
from masters.views.products_category_views import *

urlpatterns = [
    path('categories/', ProductCategoryListCreateView.as_view(), name='product-category-list-create'),
    path('categories/<int:pk>/', ProductCategoryRetrieveUpdateDeleteView.as_view(), name='product-category-detail'),
]
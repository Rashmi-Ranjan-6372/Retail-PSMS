from django.urls import path
from masters.views.suppliers_views import *
urlpatterns = [
    path('suppliers/', SupplierListAPIView.as_view()),
    path('suppliers/create/', SupplierCreateAPIView.as_view()),
    path('suppliers/<int:pk>/', SupplierDetailAPIView.as_view()),
    path('suppliers/update/<int:pk>/', SupplierUpdateAPIView.as_view()),
    path('suppliers/deactivate/<int:pk>/', SupplierSoftDeleteAPIView.as_view()),
    path('suppliers/delete/<int:pk>/', SupplierDeleteAPIView.as_view()),
]
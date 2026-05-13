from django.urls import path
from masters.views.suppliers_views import *
urlpatterns = [
    path('suppliers/', SupplierListView.as_view()),
    path('suppliers/create/', SupplierCreateView.as_view()),
    path('suppliers/<int:pk>/', SupplierDetailView.as_view()),
    path('suppliers/update/<int:pk>/', SupplierUpdateView.as_view()),
    path('suppliers/deactivate/<int:pk>/', SupplierSoftDeleteView.as_view()),
    path('suppliers/delete/<int:pk>/', SupplierDeleteView.as_view()),
]
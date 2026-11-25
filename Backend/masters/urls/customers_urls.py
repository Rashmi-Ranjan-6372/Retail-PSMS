from django.urls import path
from masters.views.customers_views import (
    CustomerActivateAPIView,
    CustomerDeactivateAPIView,
    CustomerDetailAPIView,
    CustomerHardDeleteAPIView,
    CustomerListCreateAPIView,
    InactiveCustomerListAPIView,
)
urlpatterns = [
    path("customers/", CustomerListCreateAPIView.as_view(), name="customer-list-create"),
    path("customers/<int:pk>/", CustomerDetailAPIView.as_view(), name="customer-detail"),
    path("customers/activate/<int:pk>/", CustomerActivateAPIView.as_view(), name="customer-activate"),
    path("customers/deactivate/<int:pk>/", CustomerDeactivateAPIView.as_view(), name="customer-deactivate"),
    path("customers/hard-delete/<int:pk>/", CustomerHardDeleteAPIView.as_view(), name="customer-hard-delete"),
    path("customers/inactive/", InactiveCustomerListAPIView.as_view(), name="inactive-customers"),
]
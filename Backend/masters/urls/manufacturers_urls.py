from django.urls import path
from .manufacturer_views import *
from Backend.masters.views.manufacturers_views import *

urlpatterns = [
    path('manufacturers/', ManufacturerListView.as_view()),
    path('manufacturers/create/', ManufacturerCreateView.as_view()),
    path('manufacturers/<int:pk>/', ManufacturerDetailView.as_view()),
    path('manufacturers/update/<int:pk>/', ManufacturerUpdateView.as_view()),
    path('manufacturers/deactivate/<int:pk>/', ManufacturerSoftDeleteView.as_view()),
    path('manufacturers/delete/<int:pk>/', ManufacturerDeleteView.as_view()),
]
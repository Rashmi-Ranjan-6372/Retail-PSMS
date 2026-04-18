from django.urls import path
from .manufacturer_views import *
from Backend.masters.views.manufacturers_views import *

urlpatterns = [
    path('', ManufacturerListView.as_view()),
    path('create/', ManufacturerCreateView.as_view()),
    path('<int:pk>/', ManufacturerDetailView.as_view()),
    path('<int:pk>/update/', ManufacturerUpdateView.as_view()),
    path('<int:pk>/deactivate/', ManufacturerSoftDeleteView.as_view()),
    path('<int:pk>/delete/', ManufacturerDeleteView.as_view()),
]
from django.urls import path

from inventory.views.expiry_damage_views import (
    ExpiryDamageListCreateView,
    ExpiryDamageDetailView,
)

urlpatterns = [
    path("expiry-damage/",ExpiryDamageListCreateView.as_view(),name="expiry-damage-list-create"),
    path("expiry-damage/<int:pk>/",ExpiryDamageDetailView.as_view(),name="expiry-damage-detail"),
]
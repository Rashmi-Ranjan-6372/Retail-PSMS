from django.urls import path
from masters.views.sales_offer_views import *

urlpatterns = [
    path("sales-offers/create/", SalesOfferCreateView.as_view(), name="sales-offer-create"),
    path("sales-offers/", SalesOfferListView.as_view(), name="sales-offer-list"),
    path("sales-offers/<int:pk>/", SalesOfferDetailView.as_view(), name="sales-offer-detail"),
    path("sales-offers/update/<int:pk>/", SalesOfferUpdateView.as_view(), name="sales-offer-update"),
    path("sales-offers/deactivate/<int:pk>/", SalesOfferSoftDeleteView.as_view(), name="sales-offer-soft-delete"),
    path("sales-offers/delete/<int:pk>/", SalesOfferDeleteView.as_view(), name="sales-offer-delete"),
]
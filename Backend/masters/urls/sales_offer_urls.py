from django.urls import path
from masters.views.sales_offer_views import *

urlpatterns = [
    path("sales-offers/create/", SalesOfferCreateAPIView.as_view(), name="sales-offer-create"),
    path("sales-offers/", SalesOfferListAPIView.as_view(), name="sales-offer-list"),
    path("sales-offers/<int:pk>/", SalesOfferDetailAPIView.as_view(), name="sales-offer-detail"),
    path("sales-offers/update/<int:pk>/", SalesOfferUpdateAPIView.as_view(), name="sales-offer-update"),
    path("sales-offers/deactivate/<int:pk>/", SalesOfferSoftDeleteAPIView.as_view(), name="sales-offer-soft-delete"),
    path("sales-offers/delete/<int:pk>/", SalesOfferDeleteAPIView.as_view(), name="sales-offer-delete"),
]
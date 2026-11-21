
from django.urls import path

from .views import (
    PlatformEmailConfigurationAPIView,
    RetailerEmailConfigurationAPIView,
    PlatformSMTPTestAPIView,
    RetailerSMTPTestAPIView
)


urlpatterns = [
    path("platform/",PlatformEmailConfigurationAPIView.as_view(),name="platform-email-configuration"),
    path("platform/test/",PlatformSMTPTestAPIView.as_view(),name="platform-smtp-test"),
    path("retailer/",RetailerEmailConfigurationAPIView.as_view(),name="retailer-email-configuration"),
    path("retailer/test/",RetailerSMTPTestAPIView.as_view(),name="retailer-smtp-test"),
]

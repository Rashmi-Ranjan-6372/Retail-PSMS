# inventory/urls/payment_urls.py

from rest_framework.routers import DefaultRouter
from inventory.views.payment_views import (
    PaymentViewSet
)

router = DefaultRouter()
router.register(
    r'payments',
    PaymentViewSet,
    basename='payment'
)

urlpatterns = router.urls
# inventory/urls/receipt_urls.py

from rest_framework.routers import DefaultRouter
from inventory.views.receipt_views import (
    ReceiptViewSet
)

router = DefaultRouter()
router.register(
    r'receipts',
    ReceiptViewSet,
    basename='receipt'
)

urlpatterns = router.urls
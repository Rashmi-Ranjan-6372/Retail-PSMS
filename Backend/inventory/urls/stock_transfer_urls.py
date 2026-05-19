# inventory/urls/stock_transfer_urls.py

from rest_framework.routers import DefaultRouter
from inventory.views.stock_transfer_views import (
    StockTransferViewSet
)

router = DefaultRouter()
router.register(
    r'stock-transfers',
    StockTransferViewSet,
    basename='stock-transfer'
)

urlpatterns = router.urls
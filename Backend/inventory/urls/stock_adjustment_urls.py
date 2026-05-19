# inventory/urls/stock_adjustment_urls.py

from rest_framework.routers import DefaultRouter
from inventory.views.stock_adjustment_views import (
    StockAdjustmentViewSet
)

router = DefaultRouter()
router.register(
    r'stock-adjustments',
    StockAdjustmentViewSet,
    basename='stock-adjustment'
)

urlpatterns = router.urls
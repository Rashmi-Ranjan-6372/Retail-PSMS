# inventory/urls/stock_batch_urls.py

from rest_framework.routers import DefaultRouter
from inventory.views.stock_batch_views import (
    StockBatchViewSet
)

router = DefaultRouter()
router.register(
    r'stock-batches',
    StockBatchViewSet,
    basename='stock-batch'
)

urlpatterns = router.urls
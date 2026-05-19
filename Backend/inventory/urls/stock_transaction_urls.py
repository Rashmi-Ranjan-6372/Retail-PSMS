# inventory/urls/stock_transaction_urls.py

from rest_framework.routers import DefaultRouter
from inventory.views.stock_transaction_views import (
    StockTransactionViewSet
)

router = DefaultRouter()
router.register(
    r'stock-transactions',
    StockTransactionViewSet,
    basename='stock-transaction'
)

urlpatterns = router.urls
# inventory/urls/sales_urls.py

from rest_framework.routers import DefaultRouter
from inventory.views.sales_views import (
    SalesViewSet
)

router = DefaultRouter()
router.register(
    r'sales',
    SalesViewSet,
    basename='sales'
)

urlpatterns = router.urls
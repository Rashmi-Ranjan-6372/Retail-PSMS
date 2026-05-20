from rest_framework.routers import DefaultRouter
from inventory.views.expiry_damage_views import (
    ExpiryDamageViewSet
)

router = DefaultRouter()
router.register(
    r'expiry-damages',
    ExpiryDamageViewSet,
    basename='expiry-damage'
)

urlpatterns = router.urls
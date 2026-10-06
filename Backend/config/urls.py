from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('accounts.urls')),
    path('branches/', include('branches.urls')),
    path('masters/', include('masters.urls')),
    path('inventory/', include('inventory.urls')),
    path('reports/', include('reports.urls')),
    path('settings/', include('settings.urls')),
    path('backups/', include('backups.urls')),
    path('subscriptions/', include('subscriptions.urls')),
    path('supports/', include('support.urls')),
]
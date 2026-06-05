from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/branches/', include('branches.urls')),
    path('api/masters/', include('masters.urls')),
    path('api/inventory/', include('inventory.urls')),
    path('api/reports/', include('reports.urls')),
    path('api/settings/', include('settings.urls')),
    path('api/backups/', include('backups.urls')),
]
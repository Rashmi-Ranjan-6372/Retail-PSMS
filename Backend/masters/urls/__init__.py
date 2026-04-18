from django.urls import path, include

urlpatterns = [
    # path('products/', include('masters.urls.products_urls')),
    path('suppliers/', include('masters.urls.suppliers_urls')),
    # path('sales-offers/', include('masters.urls.sales_offer_urls')),
]
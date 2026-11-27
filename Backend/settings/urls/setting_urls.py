
from django.urls import path

from settings.views.setting_views import (
    FinancialYearView,
    GeneralSettingView
)


urlpatterns = [
    path("financial-years/",FinancialYearView.as_view(),name="financial-year-list-create"),
    path("financial-years/<int:pk>/",FinancialYearView.as_view(),name="financial-year-detail"),
    path("general-settings/",GeneralSettingView.as_view(),name="general-settings"),
]

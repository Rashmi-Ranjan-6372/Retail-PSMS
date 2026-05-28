from django.urls import path

from settings.views.financial_year_view import (
    FinancialYearView
)

urlpatterns = [

    path("financial-years/", FinancialYearView.as_view(), name="financial-year-list-create"),
    path("financial-years/<int:pk>/", FinancialYearView.as_view(), name="financial-year-detail"),
]
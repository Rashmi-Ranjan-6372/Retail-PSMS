from django.urls import path
from reports.views.analytics_view import AnalyticsView

urlpatterns = [
    path("analytics/", AnalyticsView.as_view(), name="analytics-report"),
]
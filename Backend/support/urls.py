from django.urls import path

from .views import (
    CreateSupportTicketView,
    SupportTicketListView,
    SupportTicketDetailView,
    ReplyTicketView,
    UpdateTicketStatusView,
    SupportDashboardView,
)

urlpatterns = [
    path("tickets/create/",CreateSupportTicketView.as_view()),
    path("tickets/",SupportTicketListView.as_view()),
    path("tickets/<int:pk>/",SupportTicketDetailView.as_view()),
    path("tickets/<int:pk>/reply/",ReplyTicketView.as_view()),
    path("tickets/<int:pk>/status/",UpdateTicketStatusView.as_view()),
    path("dashboard/",SupportDashboardView.as_view()),
]
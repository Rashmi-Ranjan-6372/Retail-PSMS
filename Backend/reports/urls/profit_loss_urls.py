from django.urls import path
from reports.views.profit_loss_view import ProfitLossView

urlpatterns = [
    path("profit-loss/", ProfitLossView.as_view(), name="profit-loss-report"),
]
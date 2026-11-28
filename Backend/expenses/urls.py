
from django.urls import path

from .views import (
    ExpenseListCreateView,
    ExpenseDetailView,
    ExpenseCategoryListCreateView,
    ApproveExpenseView,
    MarkExpensePaidView,
    CancelExpenseView,
)


urlpatterns = [
    path("categories/",ExpenseCategoryListCreateView.as_view(),name="expense-category-list-create",),
    path("",ExpenseListCreateView.as_view(),name="expense-list-create",),
    path("<int:pk>/",ExpenseDetailView.as_view(),name="expense-detail",),
    path("<int:pk>/approve/",ApproveExpenseView.as_view(),name="expense-approve",),
    path("<int:pk>/pay/",MarkExpensePaidView.as_view(),name="expense-pay",),
    path("<int:pk>/cancel/",CancelExpenseView.as_view(),name="expense-cancel",),
]

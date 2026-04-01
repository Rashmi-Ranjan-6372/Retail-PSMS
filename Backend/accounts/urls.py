from django.urls import path
from .views import AdminResetPasswordView, LoginView, LogoutAllDevicesView, LogoutAllExceptOwnView, ProfileView, CreateStaffView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('logout-all/', LogoutAllDevicesView.as_view()),
    path('logout-all-except-own/', LogoutAllExceptOwnView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('create-staff/', CreateStaffView.as_view()),
    path('admin-reset-password/', AdminResetPasswordView.as_view()),
]
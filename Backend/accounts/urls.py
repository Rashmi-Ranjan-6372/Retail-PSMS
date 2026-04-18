from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('logout-all/', LogoutAllDevicesView.as_view()),
    path('logout-all-except-own/', LogoutAllExceptOwnView.as_view()),
    path("logout-branch/", LogoutBranchView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('create-staff/', CreateStaffView.as_view()),
    path('admin-reset-password/', AdminResetPasswordView.as_view()),
    path('token/refresh/', CustomTokenRefreshView.as_view()),
    path('user/deactivate/<int:user_id>/', DeactivateUserView.as_view()),
    path('user/reactivate/<int:user_id>/', ReactivateUserView.as_view()),
    path('user/delete/<int:user_id>/', DeleteUserView.as_view()),
    path('users/', UserListView.as_view()),
    path('users/bulk-action/', BulkUserActionView.as_view()),
    path('users/filter/', UserFilterView.as_view()),
]

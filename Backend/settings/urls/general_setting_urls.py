from django.urls import path

from settings.views.general_setting_view import (
    GeneralSettingView
)

urlpatterns = [
    path("general-settings/", GeneralSettingView.as_view(), name="general-settings"),
]
from rest_framework import serializers

from settings.models.general_setting_models import (
    GeneralSetting
)


class GeneralSettingSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = GeneralSetting

        fields = "__all__"

        read_only_fields = (
            "created_at",
            "updated_at",
        )
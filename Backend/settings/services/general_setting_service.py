from settings.models.general_setting_models import (
    GeneralSetting
)


class GeneralSettingService:

    @staticmethod
    def get_settings(retailer):

        return GeneralSetting.objects.filter(
            retailer=retailer
        ).first()

    @staticmethod
    def create_or_update_settings(
        retailer,
        validated_data,
        user=None
    ):

        settings_obj, created = (
            GeneralSetting.objects.update_or_create(
                retailer=retailer,
                defaults={
                    **validated_data,
                    "created_by": user
                }
            )
        )

        return settings_obj
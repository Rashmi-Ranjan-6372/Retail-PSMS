from django.db import transaction

from settings.models.models import FinancialYear, GeneralSetting

class FinancialYearService:

    @staticmethod
    def get_all(retailer, branch=None):

        queryset = FinancialYear.objects.filter(retailer=retailer)

        if branch is not None:
            queryset = queryset.filter(branch=branch)

        return queryset.order_by("-id")

    @staticmethod
    def create_financial_year(validated_data, retailer, user=None):

        with transaction.atomic():

            financial_year = FinancialYear.objects.create(
                **validated_data, retailer=retailer, created_by=user
            )

        return financial_year

    @staticmethod
    def update_financial_year(instance, validated_data):

        with transaction.atomic():

            for key, value in validated_data.items():
                setattr(instance, key, value)

            instance.save()

        return instance

    @staticmethod
    def delete_financial_year(instance):

        with transaction.atomic():
            instance.delete()

    @staticmethod
    def get_active_financial_year(retailer, branch=None):

        queryset = FinancialYear.objects.filter(retailer=retailer, is_active=True)

        if branch is not None:

            branch_year = queryset.filter(branch=branch).first()

            if branch_year:
                return branch_year

            return queryset.filter(branch__isnull=True).first()

        return queryset.filter(branch__isnull=True).first()


class GeneralSettingService:

    @staticmethod
    def get_settings(retailer):

        return GeneralSetting.objects.filter(retailer=retailer).first()

    @staticmethod
    def create_or_update_settings(retailer, validated_data, user=None):

        with transaction.atomic():

            settings_obj, created = GeneralSetting.objects.get_or_create(
                retailer=retailer, defaults={**validated_data, "created_by": user}
            )

            if not created:

                for key, value in validated_data.items():
                    setattr(settings_obj, key, value)

                settings_obj.save()

        return settings_obj, created

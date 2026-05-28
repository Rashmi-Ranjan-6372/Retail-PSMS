from settings.models.financial_year_models import (
    FinancialYear
)


class FinancialYearService:

    @staticmethod
    def get_all(retailer, branch=None):

        queryset = FinancialYear.objects.filter(
            retailer=retailer
        )

        if branch:

            queryset = queryset.filter(
                branch=branch
            )

        return queryset.order_by("-id")

    @staticmethod
    def create_financial_year(
        validated_data,
        user=None
    ):

        financial_year = FinancialYear.objects.create(
            **validated_data,
            created_by=user
        )

        return financial_year

    @staticmethod
    def update_financial_year(
        instance,
        validated_data
    ):

        for key, value in validated_data.items():

            setattr(instance, key, value)

        instance.save()

        return instance

    @staticmethod
    def delete_financial_year(instance):

        instance.delete()

    @staticmethod
    def get_active_financial_year(
        retailer,
        branch=None
    ):

        queryset = FinancialYear.objects.filter(
            retailer=retailer,
            is_active=True
        )

        if branch:

            queryset = queryset.filter(
                branch=branch
            )

        return queryset.first()
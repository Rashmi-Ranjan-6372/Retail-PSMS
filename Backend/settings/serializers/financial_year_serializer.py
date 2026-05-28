from rest_framework import serializers

from settings.models.financial_year_models import (
    FinancialYear
)


class FinancialYearSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = FinancialYear

        fields = "__all__"

        read_only_fields = (
            "created_at",
            "updated_at",
        )
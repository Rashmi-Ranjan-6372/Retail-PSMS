from rest_framework import serializers

from settings.models.models import FinancialYear, GeneralSetting

class FinancialYearSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinancialYear
        fields = "__all__"

        read_only_fields = (
            "id",
            "retailer",
            "created_by",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):

        start_date = attrs.get("start_date", getattr(self.instance, "start_date", None))

        end_date = attrs.get("end_date", getattr(self.instance, "end_date", None))

        if start_date and end_date and start_date >= end_date:
            raise serializers.ValidationError(
                {"end_date": "End date must be greater than start date."}
            )

        branch = attrs.get("branch", getattr(self.instance, "branch", None))

        retailer = self.context.get("retailer")

        if branch and retailer:
            if branch.retailer_id != retailer.id:
                raise serializers.ValidationError(
                    {"branch": "Selected branch does not belong to your retailer."}
                )

        return attrs


class GeneralSettingSerializer(serializers.ModelSerializer):

    class Meta:
        model = GeneralSetting
        fields = "__all__"

        read_only_fields = (
            "id",
            "retailer",
            "created_by",
            "created_at",
            "updated_at",
        )

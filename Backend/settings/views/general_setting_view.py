from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from settings.models.general_setting_models import (
    GeneralSetting
)

from settings.serializers.general_setting_serializer import (
    GeneralSettingSerializer
)

from settings.services.general_setting_service import (
    GeneralSettingService
)

from accounts.permissions import (
    IsAdmin,
    IsSameRetailer
)


class GeneralSettingView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin,
        IsSameRetailer
    ]

    # =========================
    # GET SETTINGS
    # =========================

    def get(self, request):

        retailer = request.user.retailer

        settings_obj = (
            GeneralSettingService.get_settings(
                retailer=retailer
            )
        )

        if not settings_obj:

            return Response(
                {
                    "success": False,
                    "message": "Settings not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = GeneralSettingSerializer(
            settings_obj
        )

        return Response(
            {
                "success": True,
                "message": "Settings fetched successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    # =========================
    # CREATE SETTINGS
    # =========================

    def post(self, request):

        serializer = GeneralSettingSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        settings_obj = (
            GeneralSettingService.create_or_update_settings(
                retailer=request.user.retailer,
                validated_data=serializer.validated_data,
                user=request.user
            )
        )

        response_serializer = (
            GeneralSettingSerializer(
                settings_obj
            )
        )

        return Response(
            {
                "success": True,
                "message": "Settings created successfully",
                "data": response_serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    # =========================
    # UPDATE SETTINGS
    # =========================

    def put(self, request):

        retailer = request.user.retailer

        settings_obj = (
            GeneralSetting.objects.filter(
                retailer=retailer
            ).first()
        )

        if not settings_obj:

            return Response(
                {
                    "success": False,
                    "message": "Settings not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = GeneralSettingSerializer(
            settings_obj,
            data=request.data,
            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            {
                "success": True,
                "message": "Settings updated successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
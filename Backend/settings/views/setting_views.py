from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from settings.models import GeneralSetting, FinancialYear

from settings.serializers.serializers import FinancialYearSerializer, GeneralSettingSerializer

from settings.services.services import FinancialYearService, GeneralSettingService

from accounts.permissions import IsAdmin, IsSameRetailerAndBranch, IsSameRetailer
from accounts.views import create_audit_log


class FinancialYearView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin, IsSameRetailerAndBranch]

    # =========================
    # GET FINANCIAL YEARS
    # =========================
    def get(self, request):

        retailer = request.user.retailer
        branch = request.user.branch

        if not retailer:
            return Response(
                {"success": False, "message": "Retailer not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = FinancialYear.objects.filter(retailer=retailer)

        # Branch users can view their branch years
        # and retailer-wide financial years.
        if branch:
            queryset = queryset.filter(Q(branch=branch) | Q(branch__isnull=True))
        else:
            queryset = queryset.filter(branch__isnull=True)

        queryset = queryset.order_by("-start_date")

        serializer = FinancialYearSerializer(queryset, many=True)

        create_audit_log(
            user=request.user,
            action="view",
            model_name="FinancialYear",
            object_id=None,
            description=(
                f"Viewed Financial Years "
                f"(Retailer: {retailer.id}, "
                f"Branch: {branch.id if branch else None})"
            ),
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Financial years fetched successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    # =========================
    # CREATE FINANCIAL YEAR
    # =========================
    def post(self, request):

        retailer = request.user.retailer
        branch = request.user.branch

        if not retailer:
            return Response(
                {"success": False, "message": "Retailer not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = FinancialYearSerializer(
            data=request.data, context={"request": request, "retailer": retailer}
        )

        serializer.is_valid(raise_exception=True)

        # Branch is assigned from the logged-in user.
        # Client cannot create a financial year for another branch.
        validated_data = serializer.validated_data
        validated_data.pop("branch", None)
        validated_data["branch"] = branch

        financial_year = FinancialYearService.create_financial_year(
            validated_data=validated_data, retailer=retailer, user=request.user
        )

        response_serializer = FinancialYearSerializer(financial_year)

        create_audit_log(
            user=request.user,
            action="create",
            model_name="FinancialYear",
            object_id=financial_year.id,
            description=(f"Created Financial Year " f"(Name: {financial_year.name})"),
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Financial year created successfully",
                "data": response_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    # =========================
    # UPDATE FINANCIAL YEAR
    # =========================
    def put(self, request, pk):

        retailer = request.user.retailer
        branch = request.user.branch

        queryset = FinancialYear.objects.filter(id=pk, retailer=retailer)

        # A branch user can update only their own branch's
        # financial year, not the retailer-wide financial year.
        if branch:
            queryset = queryset.filter(branch=branch)
        else:
            queryset = queryset.filter(branch__isnull=True)

        instance = queryset.first()

        if not instance:
            return Response(
                {"success": False, "message": "Financial year not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = FinancialYearSerializer(
            instance,
            data=request.data,
            partial=True,
            context={"request": request, "retailer": retailer},
        )

        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        # Prevent changing the financial year's ownership.
        validated_data.pop("retailer", None)
        validated_data.pop("created_by", None)
        validated_data.pop("branch", None)

        financial_year = FinancialYearService.update_financial_year(
            instance=instance, validated_data=validated_data
        )

        response_serializer = FinancialYearSerializer(financial_year)

        create_audit_log(
            user=request.user,
            action="update",
            model_name="FinancialYear",
            object_id=financial_year.id,
            description=(f"Updated Financial Year " f"(ID: {financial_year.id})"),
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Financial year updated successfully",
                "data": response_serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    # =========================
    # DELETE FINANCIAL YEAR
    # =========================
    def delete(self, request, pk):

        retailer = request.user.retailer
        branch = request.user.branch

        queryset = FinancialYear.objects.filter(id=pk, retailer=retailer)

        if branch:
            queryset = queryset.filter(branch=branch)
        else:
            queryset = queryset.filter(branch__isnull=True)

        instance = queryset.first()

        if not instance:
            return Response(
                {"success": False, "message": "Financial year not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        financial_year_id = instance.id

        FinancialYearService.delete_financial_year(instance=instance)

        create_audit_log(
            user=request.user,
            action="delete",
            model_name="FinancialYear",
            object_id=financial_year_id,
            description=(f"Deleted Financial Year " f"(ID: {financial_year_id})"),
            request=request,
        )

        return Response(
            {"success": True, "message": "Financial year deleted successfully"},
            status=status.HTTP_200_OK,
        )


class GeneralSettingView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin, IsSameRetailer]

    # =========================
    # GET SETTINGS
    # =========================
    def get(self, request):

        retailer = request.user.retailer

        if not retailer:
            return Response(
                {"success": False, "message": "Retailer not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        settings_obj = GeneralSettingService.get_settings(retailer=retailer)

        if not settings_obj:
            return Response(
                {"success": False, "message": "Settings not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = GeneralSettingSerializer(settings_obj)

        create_audit_log(
            user=request.user,
            action="view",
            model_name="GeneralSetting",
            object_id=settings_obj.id,
            description=(f"Viewed General Settings " f"(Retailer: {retailer.id})"),
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Settings fetched successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    # =========================
    # CREATE SETTINGS
    # =========================
    def post(self, request):

        retailer = request.user.retailer

        if not retailer:
            return Response(
                {"success": False, "message": "Retailer not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = GeneralSettingSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        settings_obj, created = GeneralSettingService.create_or_update_settings(
            retailer=retailer,
            validated_data=serializer.validated_data,
            user=request.user,
        )

        response_serializer = GeneralSettingSerializer(settings_obj)

        create_audit_log(
            user=request.user,
            action="create" if created else "update",
            model_name="GeneralSetting",
            object_id=settings_obj.id,
            description=(
                f"{'Created' if created else 'Updated'} "
                f"General Settings (Retailer: {retailer.id})"
            ),
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": (
                    "Settings created successfully"
                    if created
                    else "Settings updated successfully"
                ),
                "data": response_serializer.data,
            },
            status=(status.HTTP_201_CREATED if created else status.HTTP_200_OK),
        )

    # =========================
    # UPDATE SETTINGS
    # =========================
    def put(self, request):

        retailer = request.user.retailer

        if not retailer:
            return Response(
                {"success": False, "message": "Retailer not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        settings_obj = GeneralSettingService.get_settings(retailer=retailer)

        if not settings_obj:
            return Response(
                {"success": False, "message": "Settings not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = GeneralSettingSerializer(
            settings_obj, data=request.data, partial=True
        )

        serializer.is_valid(raise_exception=True)

        updated_settings, created = GeneralSettingService.create_or_update_settings(
            retailer=retailer,
            validated_data=serializer.validated_data,
            user=request.user,
        )

        response_serializer = GeneralSettingSerializer(updated_settings)

        create_audit_log(
            user=request.user,
            action="update",
            model_name="GeneralSetting",
            object_id=updated_settings.id,
            description=(f"Updated General Settings " f"(Retailer: {retailer.id})"),
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Settings updated successfully",
                "data": response_serializer.data,
            },
            status=status.HTTP_200_OK,
        )

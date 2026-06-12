from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from settings.models.financial_year_models import FinancialYear
from settings.serializers.financial_year_serializer import FinancialYearSerializer
from settings.services.financial_year_service import FinancialYearService

from accounts.permissions import IsAdmin, IsSameRetailerAndBranch
from accounts.views import create_audit_log


class FinancialYearView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin,
        IsSameRetailerAndBranch
    ]

    # =========================
    # GET FINANCIAL YEARS
    # =========================
    def get(self, request):

        retailer = request.user.retailer
        branch = request.user.branch

        queryset = FinancialYearService.get_all(
            retailer=retailer,
            branch=branch
        )

        serializer = FinancialYearSerializer(queryset, many=True)

        create_audit_log(
            user=request.user,
            action="view",
            model_name="FinancialYear",
            object_id=None,
            description=(
                f"Viewed Financial Years "
                f"(Retailer: {retailer.id if retailer else None}, "
                f"Branch: {branch.id if branch else None})"
            ),
            request=request
        )

        return Response(
            {
                "success": True,
                "message": "Financial years fetched successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    # =========================
    # CREATE FINANCIAL YEAR
    # =========================
    def post(self, request):

        serializer = FinancialYearSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        financial_year = FinancialYearService.create_financial_year(
            validated_data=serializer.validated_data,
            user=request.user
        )

        response_serializer = FinancialYearSerializer(financial_year)

        create_audit_log(
            user=request.user,
            action="create",
            model_name="FinancialYear",
            object_id=financial_year.id,
            description=(
                f"Created Financial Year "
                f"(Name: {getattr(financial_year, 'name', '')})"
            ),
            request=request
        )

        return Response(
            {
                "success": True,
                "message": "Financial year created successfully",
                "data": response_serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    # =========================
    # UPDATE FINANCIAL YEAR
    # =========================
    def put(self, request, pk):

        try:
            instance = FinancialYear.objects.get(
                id=pk,
                retailer=request.user.retailer
            )
        except FinancialYear.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Financial year not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = FinancialYearSerializer(
            instance,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        financial_year = FinancialYearService.update_financial_year(
            instance=instance,
            validated_data=serializer.validated_data
        )

        response_serializer = FinancialYearSerializer(financial_year)

        create_audit_log(
            user=request.user,
            action="update",
            model_name="FinancialYear",
            object_id=financial_year.id,
            description=(
                f"Updated Financial Year "
                f"(ID: {financial_year.id})"
            ),
            request=request
        )

        return Response(
            {
                "success": True,
                "message": "Financial year updated successfully",
                "data": response_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # =========================
    # DELETE FINANCIAL YEAR
    # =========================
    def delete(self, request, pk):

        try:
            instance = FinancialYear.objects.get(
                id=pk,
                retailer=request.user.retailer
            )
        except FinancialYear.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Financial year not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        financial_year_id = instance.id

        FinancialYearService.delete_financial_year(
            instance=instance
        )

        create_audit_log(
            user=request.user,
            action="delete",
            model_name="FinancialYear",
            object_id=financial_year_id,
            description=(
                f"Deleted Financial Year (ID: {financial_year_id})"
            ),
            request=request
        )

        return Response(
            {
                "success": True,
                "message": "Financial year deleted successfully"
            },
            status=status.HTTP_200_OK
        )
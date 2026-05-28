from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from settings.models.financial_year_models import (
    FinancialYear
)

from settings.serializers.financial_year_serializer import (
    FinancialYearSerializer
)

from settings.services.financial_year_service import (
    FinancialYearService
)

from accounts.permissions import (
    IsAdmin,
    IsSameRetailerAndBranch
)


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

        queryset = (
            FinancialYearService.get_all(
                retailer=retailer,
                branch=branch
            )
        )

        serializer = FinancialYearSerializer(
            queryset,
            many=True
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

        serializer = FinancialYearSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        financial_year = (
            FinancialYearService.create_financial_year(
                validated_data=serializer.validated_data,
                user=request.user
            )
        )

        response_serializer = (
            FinancialYearSerializer(
                financial_year
            )
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

        serializer.is_valid(
            raise_exception=True
        )

        financial_year = (
            FinancialYearService.update_financial_year(
                instance=instance,
                validated_data=serializer.validated_data
            )
        )

        response_serializer = (
            FinancialYearSerializer(
                financial_year
            )
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

        FinancialYearService.delete_financial_year(
            instance=instance
        )

        return Response(
            {
                "success": True,
                "message": "Financial year deleted successfully"
            },
            status=status.HTTP_200_OK
        )
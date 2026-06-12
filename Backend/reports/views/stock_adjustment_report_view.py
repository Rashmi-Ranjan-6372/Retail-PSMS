from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from reports.services.stock_adjustment_report_service import StockAdjustmentReportService
from accounts.views import create_audit_log


class StockAdjustmentReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        retailer_id = request.query_params.get("retailer")

        data = StockAdjustmentReportService.get_report(
            retailer_id=retailer_id
        )

        create_audit_log(
            user=request.user,
            action="view",
            model_name="StockAdjustmentReport",
            object_id=retailer_id,
            description=(
                f"Viewed Stock Adjustment Report "
                f"(Retailer: {retailer_id})"
            ),
            request=request
        )

        return Response(
            data,
            status=status.HTTP_200_OK
        )
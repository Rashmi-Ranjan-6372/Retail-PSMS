from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from reports.services.low_stock_report_service import (LowStockReportService)
from accounts.views import create_audit_log

class LowStockReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        retailer_id = request.query_params.get(
            "retailer"
        )

        branch_id = request.query_params.get(
            "branch"
        )

        data = LowStockReportService.get_report(
            retailer_id=retailer_id,
            branch_id=branch_id
        )

        create_audit_log(
            user=request.user,
            action="view",
            model_name="LowStockReport",
            object_id=retailer_id or branch_id,
            description=(
                f"Viewed Low Stock Report "
                f"(Retailer: {retailer_id}, "
                f"Branch: {branch_id})"
            ),
            request=request
        )

        return Response(
            data,
            status=status.HTTP_200_OK
        )
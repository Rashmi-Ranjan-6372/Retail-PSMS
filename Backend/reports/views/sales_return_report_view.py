from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from reports.services.sales_return_report_service import SalesReturnReportService
from accounts.views import create_audit_log
from rest_framework.permissions import IsAuthenticated


class SalesReturnReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        retailer_id = request.query_params.get("retailer")
        branch_id = request.query_params.get("branch")

        data = SalesReturnReportService.get_report(
            retailer_id=retailer_id,
            branch_id=branch_id
        )

        create_audit_log(
            user=request.user,
            action="view",
            model_name="SalesReport",
            object_id=retailer_id or branch_id,
            description=(
                f"Viewed Sales Report "
                f"(Retailer: {retailer_id}, "
                f"Branch: {branch_id})"
            ),
            request=request
        )
        return Response(data, status=status.HTTP_200_OK)
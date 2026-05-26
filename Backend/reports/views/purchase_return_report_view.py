from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from reports.services.purchase_return_report_service import PurchaseReturnReportService


class PurchaseReturnReportView(APIView):

    def get(self, request):

        retailer_id = request.query_params.get("retailer")
        branch_id = request.query_params.get("branch")

        data = PurchaseReturnReportService.get_report(
            retailer_id=retailer_id,
            branch_id=branch_id
        )

        return Response(data, status=status.HTTP_200_OK)
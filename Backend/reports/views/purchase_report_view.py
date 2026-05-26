from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from reports.services.purchase_report_service import PurchaseReportService


class PurchaseReportView(APIView):

    def get(self, request):

        retailer_id = request.query_params.get("retailer")
        branch_id = request.query_params.get("branch")

        data = PurchaseReportService.get_report(
            retailer_id=retailer_id,
            branch_id=branch_id
        )

        return Response(data, status=status.HTTP_200_OK)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from reports.services.stock_report_service import StockReportService


class StockReportView(APIView):

    def get(self, request):

        retailer_id = request.query_params.get("retailer")
        branch_id = request.query_params.get("branch")

        data = StockReportService.get_report(
            retailer_id=retailer_id,
            branch_id=branch_id
        )

        return Response(data, status=status.HTTP_200_OK)
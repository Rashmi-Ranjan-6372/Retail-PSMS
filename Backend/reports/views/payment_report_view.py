from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from reports.services.payment_report_service import PaymentReportService


class PaymentReportView(APIView):

    def get(self, request):

        retailer_id = request.query_params.get("retailer")

        data = PaymentReportService.get_report(
            retailer_id=retailer_id
        )

        return Response(data, status=status.HTTP_200_OK)
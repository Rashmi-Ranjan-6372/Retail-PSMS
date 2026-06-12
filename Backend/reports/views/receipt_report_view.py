from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from reports.services.receipt_report_service import ReceiptReportService
from accounts.views import create_audit_log
from rest_framework.permissions import IsAuthenticated


class ReceiptReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        retailer_id = request.query_params.get("retailer")

        data = ReceiptReportService.get_report(
            retailer_id=retailer_id
        )

        create_audit_log(
            user=request.user,
            action="view",
            model_name="ReceiptReport",
            object_id=retailer_id,
            description=(
                f"Viewed Receipt Report "
                f"(Retailer: {retailer_id})"
            ),
            request=request
        )

        return Response(data, status=status.HTTP_200_OK)
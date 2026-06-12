from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from reports.services.payment_report_service import PaymentReportService
from accounts.views import create_audit_log

class PaymentReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        retailer_id = request.query_params.get("retailer")

        data = PaymentReportService.get_report(
            retailer_id=retailer_id
        )

        create_audit_log(
            user=request.user,
            action="view",
            model_name="PaymentReport",
            object_id=retailer_id,
            description=(
                f"Viewed Payment Report "
                f"(Retailer: {retailer_id})"
            ),
            request=request
        )

        return Response(
            data,
            status=status.HTTP_200_OK
        )
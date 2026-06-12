from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from reports.services.gst_report_service import (GSTReportService)
from accounts.views import create_audit_log

class GSTReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        retailer_id = request.query_params.get(
            "retailer"
        )

        data = GSTReportService.get_report(
            retailer_id=retailer_id
        )

        create_audit_log(
            user=request.user,
            action="view",
            model_name="GSTReport",
            object_id=retailer_id,
            description=(
                f"Viewed GST Report "
                f"for Retailer {retailer_id}"
            ),
            request=request
        )

        return Response(
            data,
            status=status.HTTP_200_OK
        )
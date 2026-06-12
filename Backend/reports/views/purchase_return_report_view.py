from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from reports.services.purchase_return_report_service import PurchaseReturnReportService
from accounts.views import create_audit_log
from rest_framework.permissions import IsAuthenticated

class PurchaseReturnReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        retailer_id = request.query_params.get("retailer")
        branch_id = request.query_params.get("branch")

        data = PurchaseReturnReportService.get_report(
            retailer_id=retailer_id,
            branch_id=branch_id
        )

        create_audit_log(
            user=request.user,
            action="view",
            model_name="PurchaseReturnReport",
            object_id=retailer_id or branch_id,
            description=(
                f"Viewed Purchase Return Report "
                f"(Retailer: {retailer_id}, "
                f"Branch: {branch_id})"
            ),
            request=request
        )

        return Response(data, status=status.HTTP_200_OK)
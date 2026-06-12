from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from reports.services.product_ledger_service import ProductLedgerService
from accounts.views import create_audit_log


class ProductLedgerView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        product_id = request.query_params.get("product")
        retailer_id = request.query_params.get("retailer")
        branch_id = request.query_params.get("branch")

        data = ProductLedgerService.get_report(
            product_id=product_id,
            retailer_id=retailer_id,
            branch_id=branch_id
        )

        create_audit_log(
            user=request.user,
            action="view",
            model_name="ProductLedger",
            object_id=product_id or retailer_id or branch_id,
            description=(
                f"Viewed Product Ledger "
                f"(Product: {product_id}, "
                f"Retailer: {retailer_id}, "
                f"Branch: {branch_id})"
            ),
            request=request
        )

        return Response(
            data,
            status=status.HTTP_200_OK
        )
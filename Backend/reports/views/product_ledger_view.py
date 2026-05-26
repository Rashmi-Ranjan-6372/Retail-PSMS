from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from reports.services.product_ledger_service import ProductLedgerService


class ProductLedgerView(APIView):

    def get(self, request):

        product_id = request.query_params.get("product")
        retailer_id = request.query_params.get("retailer")
        branch_id = request.query_params.get("branch")

        data = ProductLedgerService.get_report(
            product_id=product_id,
            retailer_id=retailer_id,
            branch_id=branch_id
        )

        return Response(data, status=status.HTTP_200_OK)
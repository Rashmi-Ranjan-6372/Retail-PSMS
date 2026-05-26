from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from reports.services.supplier_ledger_service import SupplierLedgerService


class SupplierLedgerView(APIView):

    def get(self, request):

        supplier_id = request.query_params.get("supplier")

        data = SupplierLedgerService.get_report(
            supplier_id=supplier_id
        )

        return Response(data, status=status.HTTP_200_OK)
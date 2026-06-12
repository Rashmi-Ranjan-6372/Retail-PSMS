from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from reports.services.supplier_ledger_service import SupplierLedgerService
from accounts.views import create_audit_log


class SupplierLedgerView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        supplier_id = request.query_params.get("supplier")

        data = SupplierLedgerService.get_report(
            supplier_id=supplier_id
        )

        create_audit_log(
            user=request.user,
            action="view",
            model_name="SupplierLedger",
            object_id=supplier_id,
            description=(
                f"Viewed Supplier Ledger "
                f"(Supplier: {supplier_id})"
            ),
            request=request
        )

        return Response(
            data,
            status=status.HTTP_200_OK
        )
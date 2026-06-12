from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from reports.services.customer_ledger_service import (CustomerLedgerService)
from accounts.views import create_audit_log

class CustomerLedgerView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        customer_id = request.query_params.get(
            "customer"
        )

        data = CustomerLedgerService.get_report(
            customer_id=customer_id
        )

        create_audit_log(
            user=request.user,
            action="view",
            model_name="CustomerLedger",
            object_id=customer_id,
            description=f"Viewed Customer Ledger Report for Customer {customer_id}",
            request=request
        )

        return Response(
            data,
            status=status.HTTP_200_OK
        )
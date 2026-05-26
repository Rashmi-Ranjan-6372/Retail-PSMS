from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from reports.services.customer_ledger_service import CustomerLedgerService


class CustomerLedgerView(APIView):

    def get(self, request):

        customer_id = request.query_params.get("customer")

        data = CustomerLedgerService.get_report(
            customer_id=customer_id
        )

        return Response(data, status=status.HTTP_200_OK)
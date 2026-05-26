from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from reports.services.profit_loss_service import ProfitLossService


class ProfitLossView(APIView):

    def get(self, request):

        retailer_id = request.query_params.get("retailer")
        branch_id = request.query_params.get("branch")

        data = ProfitLossService.get_report(
            retailer_id=retailer_id,
            branch_id=branch_id
        )

        return Response(data, status=status.HTTP_200_OK)
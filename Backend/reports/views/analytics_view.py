from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from reports.services.analytics_service import AnalyticsService
from accounts.views import create_audit_log


class AnalyticsView(APIView):

    def get(self, request):

        retailer_id = request.query_params.get(
            "retailer"
        )

        data = AnalyticsService.get_report(
            retailer_id=retailer_id
        )

        create_audit_log(
            user=request.user,
            action="view",
            model_name="Analytics",
            object_id=retailer_id,
            description="Viewed Analytics Report",
            request=request
        )

        return Response(
            data,
            status=status.HTTP_200_OK
        )
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from inventory.models.sales_models import Sales
from inventory.serializers.sales_serializers import SalesSerializer
from inventory.services.sales_service import create_sale
from accounts.permissions import IsAdminOrStaff
from subscriptions.utils import check_subscription_write_access

# =====================================================
# SALES LIST + CREATE
# =====================================================

class SalesListCreateView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    # =========================
    # GET SALES LIST
    # =========================

    def get(self, request):

        user = request.user

        queryset = (
            Sales.objects
            .select_related(
                "retailer",
                "branch",
                "customer",
                "created_by",
            )
            .all()
        )

        if not (
            user.is_superuser or
            getattr(user, "role", None) == "superadmin"
        ):

            queryset = queryset.filter(
                retailer=user.retailer
            )

            if getattr(user, "branch", None):

                queryset = queryset.filter(
                    branch=user.branch
                )

        serializer = SalesSerializer(
            queryset,
            many=True
        )

        return Response(serializer.data)

    # =========================
    # CREATE SALE
    # =========================

    def post(self, request):

        if not request.user.is_superuser:
            check_subscription_write_access(
                request.user.retailer
            )

        try:

            sale = create_sale(
                retailer=request.user.retailer,
                branch=request.user.branch,
                customer=request.data.get("customer"),
                items=request.data.get("items", []),
                paid_amount=request.data.get(
                    "paid_amount", 0
                ),
                discount=request.data.get(
                    "discount", 0
                ),
                remarks=request.data.get(
                    "remarks"
                ),
                created_by=request.user,
            )

            serializer = SalesSerializer(sale)

            return Response(
                {
                    "message": (
                        "Sale created successfully"
                    ),
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:

            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )


# =====================================================
# SALES DETAIL VIEW
# =====================================================

class SalesDetailView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminOrStaff,
    ]

    # =========================
    # GET OBJECT
    # =========================

    def get_object(self, pk, user):

        queryset = (
            Sales.objects
            .select_related(
                "retailer",
                "branch",
                "customer",
                "created_by",
            )
        )

        if (
            user.is_superuser or
            getattr(user, "role", None) == "superadmin"
        ):

            return queryset.get(pk=pk)

        queryset = queryset.filter(
            retailer=user.retailer
        )

        if getattr(user, "branch", None):

            queryset = queryset.filter(
                branch=user.branch
            )

        return queryset.get(pk=pk)

    # =========================
    # RETRIEVE
    # =========================

    def get(self, request, pk):

        try:

            sale = self.get_object(
                pk,
                request.user
            )

            serializer = SalesSerializer(sale)

            return Response(serializer.data)

        except Sales.DoesNotExist:

            return Response(
                {
                    "error": "Sale not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

    # =========================
    # UPDATE
    # =========================

    def put(self, request, pk):

        if not request.user.is_superuser:
            check_subscription_write_access(
                request.user.retailer
            )

        try:

            sale = self.get_object(
                pk,
                request.user
            )

            serializer = SalesSerializer(
                sale,
                data=request.data,
                partial=True
            )

            if serializer.is_valid():

                serializer.save()

                return Response(
                    {
                        "message": (
                            "Sale updated successfully"
                        ),
                        "data": serializer.data,
                    }
                )

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        except Sales.DoesNotExist:

            return Response(
                {
                    "error": "Sale not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

    # =========================
    # DELETE
    # =========================

    def delete(self, request, pk):

        if not request.user.is_superuser:
            check_subscription_write_access(
                request.user.retailer
            )

        try:

            sale = self.get_object(
                pk,
                request.user
            )

            sale.delete()

            return Response(
                {
                    "message": (
                        "Sale deleted successfully"
                    )
                },
                status=status.HTTP_204_NO_CONTENT
            )

        except Sales.DoesNotExist:

            return Response(
                {
                    "error": "Sale not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
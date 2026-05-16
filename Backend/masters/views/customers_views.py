from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models.customers_models import Customer
from .serializers import CustomerSerializer

from accounts.permissions import (
    IsAdmin,
    IsAdminOrStaff,
)


# =========================================================
# HELPER FUNCTION
# =========================================================

def get_customer_queryset(user):

    # PLATFORM OWNER
    if user.is_superuser:
        return Customer.objects.all()

    # SUPERADMIN -> ALL RETAILER CUSTOMERS
    if user.role == "superadmin":
        return Customer.objects.filter(
            retailer=user.retailer
        )

    # ADMIN / STAFF -> ONLY BRANCH CUSTOMERS
    return Customer.objects.filter(
        retailer=user.retailer,
        branch=user.branch
    )


# =========================================================
# CUSTOMER LIST + CREATE
# =========================================================

class CustomerListCreateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    def get(self, request):

        customers = get_customer_queryset(
            request.user
        ).filter(
            is_active=True
        ).order_by("-id")

        serializer = CustomerSerializer(
            customers,
            many=True
        )

        return Response(
            {
                "status": True,
                "count": customers.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def post(self, request):

        if not (
            request.user.role in ["admin", "superadmin"]
            or request.user.is_superuser
        ):
            return Response(
                {
                    "status": False,
                    "message": "Only admin can create customer"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CustomerSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(
                retailer=request.user.retailer,
                branch=request.user.branch
            )

            return Response(
                {
                    "status": True,
                    "message": "Customer created successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "status": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


# =========================================================
# CUSTOMER DETAIL
# =========================================================

class CustomerDetailAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    def get_object(self, request, pk):

        try:
            return get_customer_queryset(
                request.user
            ).get(pk=pk)

        except Customer.DoesNotExist:
            return None

    def get(self, request, pk):

        customer = self.get_object(request, pk)

        if not customer:
            return Response(
                {
                    "status": False,
                    "message": "Customer not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CustomerSerializer(customer)

        return Response(
            {
                "status": True,
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def put(self, request, pk):

        if not (
            request.user.role in ["admin", "superadmin"]
            or request.user.is_superuser
        ):
            return Response(
                {
                    "status": False,
                    "message": "Only admin can update customer"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        customer = self.get_object(request, pk)

        if not customer:
            return Response(
                {
                    "status": False,
                    "message": "Customer not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CustomerSerializer(
            customer,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "status": True,
                    "message": "Customer updated successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                "status": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):

        if not (
            request.user.role in ["admin", "superadmin"]
            or request.user.is_superuser
        ):
            return Response(
                {
                    "status": False,
                    "message": "Only admin can update customer"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        customer = self.get_object(request, pk)

        if not customer:
            return Response(
                {
                    "status": False,
                    "message": "Customer not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CustomerSerializer(
            customer,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "status": True,
                    "message": "Customer updated successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                "status": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # =========================================================
    # SOFT DELETE
    # =========================================================

    def delete(self, request, pk):

        if not (
            request.user.role in ["admin", "superadmin"]
            or request.user.is_superuser
        ):
            return Response(
                {
                    "status": False,
                    "message": "Only admin can delete customer"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        customer = self.get_object(request, pk)

        if not customer:
            return Response(
                {
                    "status": False,
                    "message": "Customer not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        customer.is_active = False
        customer.save()

        return Response(
            {
                "status": True,
                "message": "Customer soft deleted successfully"
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# ACTIVATE CUSTOMER
# =========================================================

class CustomerActivateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, pk):

        customer = get_customer_queryset(
            request.user
        ).filter(pk=pk).first()

        if not customer:
            return Response(
                {
                    "status": False,
                    "message": "Customer not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        customer.is_active = True
        customer.save()

        return Response(
            {
                "status": True,
                "message": "Customer activated successfully"
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# DEACTIVATE CUSTOMER
# =========================================================

class CustomerDeactivateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, pk):

        customer = get_customer_queryset(
            request.user
        ).filter(pk=pk).first()

        if not customer:
            return Response(
                {
                    "status": False,
                    "message": "Customer not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        customer.is_active = False
        customer.save()

        return Response(
            {
                "status": True,
                "message": "Customer deactivated successfully"
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# HARD DELETE CUSTOMER
# =========================================================

class CustomerHardDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def delete(self, request, pk):

        customer = get_customer_queryset(
            request.user
        ).filter(pk=pk).first()

        if not customer:
            return Response(
                {
                    "status": False,
                    "message": "Customer not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        customer.delete()

        return Response(
            {
                "status": True,
                "message": "Customer permanently deleted"
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# INACTIVE CUSTOMER LIST
# =========================================================

class InactiveCustomerListAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    def get(self, request):

        customers = get_customer_queryset(
            request.user
        ).filter(
            is_active=False
        )

        serializer = CustomerSerializer(
            customers,
            many=True
        )

        return Response(
            {
                "status": True,
                "count": customers.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
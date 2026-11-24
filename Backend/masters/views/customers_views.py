from django.db import IntegrityError, transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models.customers_models import Customer, RetailerCustomer

from .serializers import (
    CustomerSerializer,
    RetailerCustomerSerializer,
)

from accounts.permissions import (
    IsAdmin,
    IsAdminOrStaff,
)

from accounts.views import create_audit_log
from subscriptions.utils import check_subscription_write_access

# ========================================================
#              CUSTOMER QUERYSET
# ========================================================


def get_customer_queryset(user):

    queryset = RetailerCustomer.objects.select_related("customer", "retailer", "branch")

    if user.is_superuser:
        return queryset

    if not user.retailer_id:
        return queryset.none()

    queryset = queryset.filter(retailer=user.retailer)

    if user.role == "superadmin":
        return queryset

    if user.branch_id:
        return queryset.filter(branch=user.branch)

    return queryset


# ========================================================
#              SUBSCRIPTION VALIDATION
# ========================================================


def check_customer_subscription(user):

    if user.is_superuser:
        return

    if not user.retailer_id:
        raise ValueError("Retailer is not associated with this account.")

    check_subscription_write_access(user.retailer)


# ========================================================
#              CUSTOMER CREATE AND LIST VIEWS
# ========================================================


class CustomerListCreateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    def get(self, request):

        customers = (
            get_customer_queryset(request.user).filter(is_active=True).order_by("-id")
        )

        serializer = RetailerCustomerSerializer(customers, many=True)

        return Response(
            {"success": True, "count": customers.count(), "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    def post(self, request):

        if not (
            request.user.role in ["admin", "superadmin"] or request.user.is_superuser
        ):
            return Response(
                {"success": False, "message": "Only admin can create customer"},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            check_customer_subscription(request.user)
        except ValueError as error:
            return Response(
                {"success": False, "message": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not request.user.is_superuser and not request.user.retailer_id:
            return Response(
                {"success": False, "message": "Retailer is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = CustomerSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        mobile = serializer.validated_data["mobile"]

        try:
            with transaction.atomic():

                customer = Customer.objects.filter(mobile=mobile).first()

                if customer is None:
                    customer = serializer.save()

                if request.user.is_superuser:
                    retailer_id = request.data.get("retailer")

                    if not retailer_id:
                        return Response(
                            {"success": False, "message": "Retailer ID is required"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                    from accounts.models import Retailer

                    retailer = Retailer.objects.filter(id=retailer_id).first()

                    if not retailer:
                        return Response(
                            {"success": False, "message": "Retailer not found"},
                            status=status.HTTP_404_NOT_FOUND,
                        )

                    branch_id = request.data.get("branch")

                    if branch_id:
                        from branches.models import Branch

                        branch = Branch.objects.filter(
                            id=branch_id, retailer=retailer
                        ).first()

                        if not branch:
                            return Response(
                                {
                                    "success": False,
                                    "message": "Invalid branch for this retailer",
                                },
                                status=status.HTTP_400_BAD_REQUEST,
                            )
                    else:
                        branch = None

                else:
                    retailer = request.user.retailer
                    branch = request.user.branch

                retailer_customer = RetailerCustomer.objects.filter(
                    retailer=retailer, customer=customer
                ).first()

                if retailer_customer:

                    return Response(
                        {
                            "success": False,
                            "message": (
                                "Customer is already associated with this retailer. "
                                "Please activate the existing customer relationship "
                                "if it is inactive."
                            ),
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                retailer_customer = RetailerCustomer.objects.create(
                    retailer=retailer, customer=customer, branch=branch, is_active=True
                )

        except IntegrityError:
            return Response(
                {
                    "success": False,
                    "message": "Customer is already associated with this retailer",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        create_audit_log(
            user=request.user,
            action="create",
            model_name="RetailerCustomer",
            object_id=retailer_customer.id,
            description=f"Associated Customer {customer.name} with retailer",
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Customer created or associated successfully",
                "data": RetailerCustomerSerializer(retailer_customer).data,
            },
            status=status.HTTP_201_CREATED,
        )


# ========================================================
#           CUSTOMER DETAIL, UPDATE, DELETE VIEWS
# ========================================================


class CustomerDetailAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    def get_object(self, request, pk):

        return get_customer_queryset(request.user).filter(pk=pk).first()

    def get(self, request, pk):

        retailer_customer = self.get_object(request, pk)

        if not retailer_customer:
            return Response(
                {"success": False, "message": "Customer not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = RetailerCustomerSerializer(retailer_customer)

        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )

    def put(self, request, pk):

        return self.update_customer(request, pk, partial=False)

    def patch(self, request, pk):

        return self.update_customer(request, pk, partial=True)

    def update_customer(self, request, pk, partial=False):

        if not (
            request.user.role in ["admin", "superadmin"] or request.user.is_superuser
        ):
            return Response(
                {"success": False, "message": "Only admin can update customer"},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            check_customer_subscription(request.user)
        except ValueError as error:
            return Response(
                {"success": False, "message": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        retailer_customer = self.get_object(request, pk)

        if not retailer_customer:
            return Response(
                {"success": False, "message": "Customer not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        customer = retailer_customer.customer

        serializer = CustomerSerializer(customer, data=request.data, partial=partial)

        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()

        create_audit_log(
            user=request.user,
            action="update",
            model_name="Customer",
            object_id=customer.id,
            description=f"Updated Customer {customer.name}",
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Customer updated successfully",
                "data": RetailerCustomerSerializer(retailer_customer).data,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk):

        if not (
            request.user.role in ["admin", "superadmin"] or request.user.is_superuser
        ):
            return Response(
                {"success": False, "message": "Only admin can delete customer"},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            check_customer_subscription(request.user)
        except ValueError as error:
            return Response(
                {"success": False, "message": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        retailer_customer = self.get_object(request, pk)

        if not retailer_customer:
            return Response(
                {"success": False, "message": "Customer not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        customer_name = retailer_customer.customer.name

        retailer_customer.is_active = False
        retailer_customer.save(update_fields=["is_active", "updated_at"])

        create_audit_log(
            user=request.user,
            action="delete",
            model_name="RetailerCustomer",
            object_id=retailer_customer.id,
            description=f"Deactivated Customer {customer_name} for this retailer",
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Customer deactivated successfully for this retailer",
            },
            status=status.HTTP_200_OK,
        )


# ========================================================
#              CUSTOMER ACTIVATE VIEW
# ========================================================


class CustomerActivateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, pk):

        try:
            check_customer_subscription(request.user)
        except ValueError as error:
            return Response(
                {"success": False, "message": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        retailer_customer = get_customer_queryset(request.user).filter(pk=pk).first()

        if not retailer_customer:
            return Response(
                {"success": False, "message": "Customer not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        retailer_customer.is_active = True
        retailer_customer.save(update_fields=["is_active", "updated_at"])

        create_audit_log(
            user=request.user,
            action="activate",
            model_name="RetailerCustomer",
            object_id=retailer_customer.id,
            description=f"Activated Customer {retailer_customer.customer.name}",
            request=request,
        )

        return Response(
            {"success": True, "message": "Customer activated successfully"},
            status=status.HTTP_200_OK,
        )


# ========================================================
#              CUSTOMER DEACTIVATE VIEW
# ========================================================


class CustomerDeactivateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, pk):

        try:
            check_customer_subscription(request.user)
        except ValueError as error:
            return Response(
                {"success": False, "message": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        retailer_customer = get_customer_queryset(request.user).filter(pk=pk).first()

        if not retailer_customer:
            return Response(
                {"success": False, "message": "Customer not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        retailer_customer.is_active = False
        retailer_customer.save(update_fields=["is_active", "updated_at"])

        create_audit_log(
            user=request.user,
            action="deactivate",
            model_name="RetailerCustomer",
            object_id=retailer_customer.id,
            description=f"Deactivated Customer {retailer_customer.customer.name}",
            request=request,
        )

        return Response(
            {"success": True, "message": "Customer deactivated successfully"},
            status=status.HTTP_200_OK,
        )


# ========================================================
#              CUSTOMER RELATIONSHIP HARD DELETE
# ========================================================


class CustomerHardDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def delete(self, request, pk):

        try:
            check_customer_subscription(request.user)
        except ValueError as error:
            return Response(
                {"success": False, "message": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        retailer_customer = get_customer_queryset(request.user).filter(pk=pk).first()

        if not retailer_customer:
            return Response(
                {"success": False, "message": "Customer not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        customer_name = retailer_customer.customer.name
        relationship_id = retailer_customer.id

        retailer_customer.delete()

        create_audit_log(
            user=request.user,
            action="hard_delete",
            model_name="RetailerCustomer",
            object_id=relationship_id,
            description=(
                f"Permanently removed Customer {customer_name} " f"from this retailer"
            ),
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Customer association permanently deleted for this retailer",
            },
            status=status.HTTP_200_OK,
        )


# ========================================================
#              INACTIVE CUSTOMER LIST VIEW
# ========================================================


class InactiveCustomerListAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    def get(self, request):

        customers = (
            get_customer_queryset(request.user).filter(is_active=False).order_by("-id")
        )

        serializer = RetailerCustomerSerializer(customers, many=True)

        return Response(
            {"success": True, "count": customers.count(), "data": serializer.data},
            status=status.HTTP_200_OK,
        )

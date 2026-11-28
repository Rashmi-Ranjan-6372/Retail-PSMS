from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import (
    PermissionDenied,
    ValidationError,
)

from .models import Expense, ExpenseCategory
from .serializers import (
    ExpenseSerializer,
    ExpenseCategorySerializer,
)

from .services import (
    is_platform_owner,
    validate_expense_access,
    approve_expense,
    mark_expense_paid,
    cancel_expense,
)


# ==========================================================
#                    COMMON HELPERS
# ==========================================================
def success_response(message, data=None, status_code=status.HTTP_200_OK):
    return Response(
        {
            "success": True,
            "message": message,
            "data": data,
        },
        status=status_code,
    )


def get_expense_queryset(user):

    queryset = Expense.objects.select_related(
        "retailer",
        "branch",
        "category",
        "created_by",
        "approved_by",
        "cancelled_by",
    )

    if is_platform_owner(user):
        return queryset.filter(scope="platform")

    if not user.retailer_id:
        return queryset.none()

    queryset = queryset.filter(
        scope="retailer",
        retailer_id=user.retailer_id,
    )

    if getattr(user, "role", None) in ("superadmin", "admin"):
        return queryset

    if not user.branch_id:
        return queryset.none()

    return queryset.filter(branch_id=user.branch_id)


def get_category_queryset(user):

    queryset = ExpenseCategory.objects.select_related(
        "retailer",
        "created_by",
    )

    if is_platform_owner(user):
        return queryset.filter(
            scope="platform",
            retailer__isnull=True,
        )

    if not user.retailer_id:
        return queryset.none()

    return queryset.filter(
        scope="retailer",
        retailer_id=user.retailer_id,
    )


def validate_create_permission(user):

    if is_platform_owner(user):
        return

    if not user.retailer_id:
        raise PermissionDenied("You are not associated with any retailer.")

    if getattr(user, "role", None) not in (
        "superadmin",
        "admin",
        "store_manager",
        "pharmacist",
        "cashier",
        "staff",
    ):
        raise PermissionDenied("You do not have permission to create expenses.")


# ==========================================================
#              EXPENSE LIST AND CREATE API
# ==========================================================
class ExpenseListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        expenses = get_expense_queryset(request.user).order_by(
            "-expense_date",
            "-created_at",
        )

        serializer = ExpenseSerializer(
            expenses,
            many=True,
            context={"request": request},
        )

        return success_response(
            "Expenses retrieved successfully.",
            serializer.data,
        )

    def post(self, request):

        validate_create_permission(request.user)

        serializer = ExpenseSerializer(
            data=request.data,
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)

        expense = serializer.save()

        return success_response(
            "Expense created successfully.",
            ExpenseSerializer(
                expense,
                context={"request": request},
            ).data,
            status.HTTP_201_CREATED,
        )


# ==========================================================
#                  EXPENSE DETAIL API
# ==========================================================
class ExpenseDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):

        expense = get_object_or_404(
            get_expense_queryset(request.user),
            pk=pk,
        )

        validate_expense_access(request.user, expense)

        return expense

    def get(self, request, pk):

        expense = self.get_object(request, pk)

        serializer = ExpenseSerializer(
            expense,
            context={"request": request},
        )

        return success_response(
            "Expense details retrieved successfully.",
            serializer.data,
        )

    def patch(self, request, pk):

        expense = self.get_object(request, pk)

        if expense.status != "draft":
            raise ValidationError("Only draft expenses can be updated.")

        if not is_platform_owner(request.user):
            if expense.created_by_id != request.user.id:
                if getattr(request.user, "role", None) not in (
                    "superadmin",
                    "admin",
                ):
                    raise PermissionDenied(
                        "You can update only expenses created by you."
                    )

        serializer = ExpenseSerializer(
            expense,
            data=request.data,
            partial=True,
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)

        expense = serializer.save()

        return success_response(
            "Expense updated successfully.",
            ExpenseSerializer(
                expense,
                context={"request": request},
            ).data,
        )


# ==========================================================
#            EXPENSE CATEGORY LIST AND CREATE API
# ==========================================================
class ExpenseCategoryListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        categories = get_category_queryset(request.user).order_by("name")

        serializer = ExpenseCategorySerializer(
            categories,
            many=True,
            context={"request": request},
        )

        return success_response(
            "Expense categories retrieved successfully.",
            serializer.data,
        )

    def post(self, request):

        if not is_platform_owner(request.user):
            if getattr(request.user, "role", None) not in (
                "superadmin",
                "admin",
            ):
                raise PermissionDenied(
                    "You do not have permission to create expense categories."
                )

        serializer = ExpenseCategorySerializer(
            data=request.data,
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)

        category = serializer.save()

        return success_response(
            "Expense category created successfully.",
            ExpenseCategorySerializer(
                category,
                context={"request": request},
            ).data,
            status.HTTP_201_CREATED,
        )


# ==========================================================
#                   APPROVE EXPENSE API
# ==========================================================
class ApproveExpenseView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        expense = approve_expense(
            expense_id=pk,
            user=request.user,
        )

        return success_response(
            "Expense approved successfully.",
            ExpenseSerializer(
                expense,
                context={"request": request},
            ).data,
        )


# ==========================================================
#                 MARK EXPENSE AS PAID API
# ==========================================================
class MarkExpensePaidView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        payment_method = request.data.get("payment_method")
        payment_reference = request.data.get(
            "payment_reference",
            "",
        )

        if not payment_method:
            raise ValidationError({"payment_method": "Payment method is required."})

        allowed_methods = dict(Expense._meta.get_field("payment_method").choices)

        if payment_method not in allowed_methods:
            raise ValidationError(
                {
                    "payment_method": (
                        "Invalid payment method. Choose one of: "
                        + ", ".join(allowed_methods.keys())
                    )
                }
            )

        expense = mark_expense_paid(
            expense_id=pk,
            user=request.user,
            payment_method=payment_method,
            payment_reference=payment_reference,
        )

        return success_response(
            "Expense marked as paid successfully.",
            ExpenseSerializer(
                expense,
                context={"request": request},
            ).data,
        )


# ==========================================================
#                    CANCEL EXPENSE API
# ==========================================================
class CancelExpenseView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        cancellation_reason = request.data.get(
            "cancellation_reason",
            "",
        )

        if not cancellation_reason.strip():
            raise ValidationError(
                {"cancellation_reason": ("Cancellation reason is required.")}
            )

        expense = cancel_expense(
            expense_id=pk,
            user=request.user,
            cancellation_reason=cancellation_reason,
        )

        return success_response(
            "Expense cancelled successfully.",
            ExpenseSerializer(
                expense,
                context={"request": request},
            ).data,
        )

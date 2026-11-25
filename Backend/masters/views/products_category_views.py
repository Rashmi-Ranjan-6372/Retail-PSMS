from django.db.models import Q
from django.db.models.deletion import ProtectedError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsAdmin
from subscriptions.utils import check_subscription_write_access

from masters.models.products_category_models import Category
from masters.serializers.products_category_serializers import ProductCategorySerializer

def get_category_queryset(user):
    queryset = Category.objects.select_related("retailer", "branch")

    if user.is_superuser:
        return queryset

    if not getattr(user, "retailer_id", None):
        return Category.objects.none()

    queryset = queryset.filter(retailer=user.retailer)

    if user.role == "superadmin":
        return queryset

    if user.branch_id:
        return queryset.filter(Q(branch=user.branch) | Q(branch__isnull=True))

    return queryset


def check_category_subscription(user):
    if user.is_superuser:
        return

    if not getattr(user, "retailer", None):
        raise ValueError("Retailer account is not assigned.")

    check_subscription_write_access(user.retailer)


class ProductCategoryListCreateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        queryset = get_category_queryset(request.user)

        is_active = request.query_params.get("is_active")

        if is_active is not None:
            if is_active.lower() not in ["true", "false"]:
                return Response(
                    {"success": False, "message": "is_active must be true or false."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            queryset = queryset.filter(is_active=(is_active.lower() == "true"))
        else:
            queryset = queryset.filter(is_active=True)

        search = request.query_params.get("search")

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(code__icontains=search)
            )

        serializer = ProductCategorySerializer(queryset, many=True)

        return Response(
            {
                "success": True,
                "message": "Categories fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        try:
            check_category_subscription(request.user)

            if request.user.is_superuser:
                retailer_id = request.data.get("retailer")

                if not retailer_id:
                    return Response(
                        {"success": False, "message": "Retailer ID is required."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                from accounts.models import Retailer
                from branches.models import Branch

                try:
                    retailer = Retailer.objects.get(id=retailer_id)
                except Retailer.DoesNotExist:
                    return Response(
                        {"success": False, "message": "Retailer not found."},
                        status=status.HTTP_404_NOT_FOUND,
                    )

                branch_id = request.data.get("branch")
                branch = None

                if branch_id:
                    try:
                        branch = Branch.objects.get(id=branch_id, retailer=retailer)
                    except Branch.DoesNotExist:
                        return Response(
                            {
                                "success": False,
                                "message": "Branch does not belong to this retailer.",
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )

            else:
                retailer = request.user.retailer
                branch = None

            serializer = ProductCategorySerializer(
                data=request.data, context={"request": request}
            )

            if serializer.is_valid():
                category = serializer.save(retailer=retailer, branch=branch)

                return Response(
                    {
                        "success": True,
                        "message": "Category created successfully.",
                        "data": ProductCategorySerializer(category).data,
                    },
                    status=status.HTTP_201_CREATED,
                )

            return Response(
                {
                    "success": False,
                    "message": "Validation failed.",
                    "data": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except ValueError as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ProductCategoryDetailAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self, pk, user):
        return get_category_queryset(user).filter(pk=pk).first()

    def get(self, request, pk):
        category = self.get_object(pk, request.user)

        if not category:
            return Response(
                {"success": False, "message": "Category not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ProductCategorySerializer(category)

        return Response(
            {
                "success": True,
                "message": "Category fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk):
        return self.update_category(request, pk, partial=False)

    def patch(self, request, pk):
        return self.update_category(request, pk, partial=True)

    def update_category(self, request, pk, partial=False):
        category = self.get_object(pk, request.user)

        if not category:
            return Response(
                {"success": False, "message": "Category not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            check_category_subscription(request.user)

            serializer = ProductCategorySerializer(
                category,
                data=request.data,
                partial=partial,
                context={"request": request},
            )

            if serializer.is_valid():
                serializer.save()

                return Response(
                    {
                        "success": True,
                        "message": "Category updated successfully.",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {
                    "success": False,
                    "message": "Validation failed.",
                    "data": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except ValueError as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ProductCategoryDeactivateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, pk):
        category = get_category_queryset(request.user).filter(pk=pk).first()

        if not category:
            return Response(
                {"success": False, "message": "Category not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            check_category_subscription(request.user)

            if not category.is_active:
                return Response(
                    {"success": False, "message": "Category is already inactive."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            category.is_active = False
            category.save(update_fields=["is_active", "updated_at"])

            return Response(
                {"success": True, "message": "Category deactivated successfully."},
                status=status.HTTP_200_OK,
            )

        except ValueError as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ProductCategoryRestoreAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, pk):
        category = get_category_queryset(request.user).filter(pk=pk).first()

        if not category:
            return Response(
                {"success": False, "message": "Category not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            check_category_subscription(request.user)

            if category.is_active:
                return Response(
                    {"success": False, "message": "Category is already active."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            category.is_active = True
            category.save(update_fields=["is_active", "updated_at"])

            return Response(
                {"success": True, "message": "Category restored successfully."},
                status=status.HTTP_200_OK,
            )

        except ValueError as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

from django.db.models import Q
from django.db.models.deletion import ProtectedError
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from masters.models import SalesOffer
from masters.serializers import SalesOfferSerializer

from accounts.permissions import IsAdmin
from subscriptions.utils import check_subscription_write_access
from accounts.views import create_audit_log

# =========================================================
# RETAILER HELPER
# =========================================================


def get_user_retailer(user):
    if user.is_superuser:
        return None

    return getattr(user, "retailer", None)


# =========================================================
# SUBSCRIPTION HELPER
# =========================================================


def check_offer_subscription(user, retailer):

    if user.is_superuser:
        return

    if not retailer:
        raise ValueError("Retailer account is not assigned.")

    check_subscription_write_access(retailer)


# =========================================================
# BRANCH VALIDATION HELPER
# =========================================================


def get_offer_branch(user, retailer, request, existing_offer=None):

    branch_id = request.data.get("branch")

    if branch_id is None and existing_offer:
        branch = existing_offer.branch

    elif branch_id is None:

        if getattr(user, "branch_id", None):
            branch = user.branch
        else:
            branch = None

    # Empty value means retailer-wide offer.
    elif branch_id == "":
        branch = None

    else:
        from branches.models import Branch

        try:
            branch = Branch.objects.get(id=branch_id, retailer=retailer)
        except (Branch.DoesNotExist, ValueError, TypeError):
            raise ValueError("Invalid branch selected.")

    if branch and branch.retailer_id != retailer.id:
        raise ValueError("Selected branch does not belong to this retailer.")

    # A branch-level user cannot create or assign an offer
    # to another branch or make it retailer-wide.
    user_branch_id = getattr(user, "branch_id", None)

    if not user.is_superuser and user_branch_id:

        if branch is None or branch.id != user_branch_id:
            raise ValueError(
                "You can only manage sales offers for your assigned branch."
            )

    return branch


# =========================================================
# BASE QUERYSET HELPER
# =========================================================


def get_sales_offer_queryset(user, request):

    queryset = SalesOffer.objects.select_related(
        "product", "category", "manufacturer", "retailer", "branch"
    )

    # =====================================================
    # PLATFORM OWNER
    # =====================================================

    if user.is_superuser:

        retailer_id = request.query_params.get("retailer")

        if retailer_id:
            queryset = queryset.filter(retailer_id=retailer_id)

        return queryset

    # =====================================================
    # RETAILER USERS
    # =====================================================

    retailer_id = getattr(user, "retailer_id", None)

    if not retailer_id:
        return queryset.none()

    queryset = queryset.filter(retailer_id=retailer_id)

    # =====================================================
    # BRANCH USER
    # =====================================================

    branch_id = getattr(user, "branch_id", None)

    if branch_id:

        # Branch users can see:
        # 1. Retailer-wide offers (branch=None)
        # 2. Offers created for their own branch

        queryset = queryset.filter(Q(branch__isnull=True) | Q(branch_id=branch_id))

    return queryset


# =========================================================
# WRITE ACCESS HELPER
# =========================================================


def can_manage_offer(user, offer):

    # Platform owner can manage all offers.
    if user.is_superuser:
        return True

    user_branch_id = getattr(user, "branch_id", None)

    # Retailer-level user can manage all offers of their retailer.
    if not user_branch_id:
        return True

    # Branch-level user can manage only their own branch offers.
    return offer.branch_id == user_branch_id


# =========================================================
# CREATE
# =========================================================


class SalesOfferCreateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):

        user = request.user

        # =================================================
        # GET RETAILER
        # =================================================

        if user.is_superuser:

            retailer_id = request.data.get("retailer")

            if not retailer_id:
                return Response(
                    {"success": False, "message": "Retailer is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            from accounts.models import Retailer

            try:
                retailer = Retailer.objects.get(id=retailer_id)
            except (Retailer.DoesNotExist, ValueError, TypeError):
                return Response(
                    {"success": False, "message": "Invalid retailer."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        else:

            retailer = get_user_retailer(user)

            if not retailer:
                return Response(
                    {"success": False, "message": "Retailer account is not assigned."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # =================================================
        # SUBSCRIPTION CHECK
        # =================================================

        check_offer_subscription(user, retailer)

        # =================================================
        # BRANCH VALIDATION
        # =================================================

        try:
            branch = get_offer_branch(user=user, retailer=retailer, request=request)
        except ValueError as error:
            return Response(
                {"success": False, "message": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # =================================================
        # SERIALIZER
        # =================================================

        serializer = SalesOfferSerializer(
            data=request.data, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        sales_offer = serializer.save(retailer=retailer, branch=branch)

        # =================================================
        # AUDIT LOG
        # =================================================

        create_audit_log(
            user=user,
            action="create",
            model_name="SalesOffer",
            object_id=sales_offer.id,
            description=f"Created Sales Offer {sales_offer.name}",
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Sales offer created successfully.",
                "data": SalesOfferSerializer(
                    sales_offer, context={"request": request}
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )


# =========================================================
# LIST
# =========================================================


class SalesOfferListAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):

        queryset = get_sales_offer_queryset(request.user, request)

        # =================================================
        # ACTIVE FILTER
        # =================================================

        is_active = request.query_params.get("is_active")

        if is_active is not None:

            if is_active.lower() not in ["true", "false"]:
                return Response(
                    {"success": False, "message": "is_active must be true or false."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            queryset = queryset.filter(is_active=(is_active.lower() == "true"))

        # =================================================
        # OFFER TYPE FILTER
        # =================================================

        offer_type = request.query_params.get("offer_type")

        if offer_type:
            queryset = queryset.filter(offer_type=offer_type)

        # =================================================
        # BRANCH FILTER
        # =================================================

        branch_id = request.query_params.get("branch")

        if branch_id:

            user = request.user
            user_branch_id = getattr(user, "branch_id", None)

            # Branch users cannot filter another branch.
            if not user.is_superuser and user_branch_id:

                if str(user_branch_id) != str(branch_id):
                    return Response(
                        {
                            "success": False,
                            "message": "You cannot access another branch's offers.",
                        },
                        status=status.HTTP_403_FORBIDDEN,
                    )

            # Include retailer-wide offers for the selected branch.
            queryset = queryset.filter(Q(branch__isnull=True) | Q(branch_id=branch_id))

        # =================================================
        # SEARCH
        # =================================================

        search = request.query_params.get("search")

        if search:
            queryset = queryset.filter(name__icontains=search)

        # =================================================
        # ORDERING
        # =================================================

        queryset = queryset.order_by("-created_at")

        serializer = SalesOfferSerializer(
            queryset, many=True, context={"request": request}
        )

        return Response(
            {"success": True, "count": queryset.count(), "data": serializer.data},
            status=status.HTTP_200_OK,
        )


# =========================================================
# DETAIL
# =========================================================


class SalesOfferDetailAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self, request, pk):

        queryset = get_sales_offer_queryset(request.user, request)

        return queryset.filter(id=pk).first()

    def get(self, request, pk):

        offer = self.get_object(request, pk)

        if not offer:
            return Response(
                {"success": False, "message": "Sales offer not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = SalesOfferSerializer(offer, context={"request": request})

        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )


# =========================================================
# UPDATE
# =========================================================


class SalesOfferUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self, request, pk):

        queryset = get_sales_offer_queryset(request.user, request)

        return queryset.filter(id=pk).first()

    def put(self, request, pk):

        return self.update_offer(request, pk, partial=False)

    def patch(self, request, pk):

        return self.update_offer(request, pk, partial=True)

    def update_offer(self, request, pk, partial=False):

        user = request.user

        offer = self.get_object(request, pk)

        if not offer:
            return Response(
                {"success": False, "message": "Sales offer not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # =================================================
        # BRANCH MANAGEMENT CHECK
        # =================================================

        if not can_manage_offer(user, offer):
            return Response(
                {"success": False, "message": "You cannot update this sales offer."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # =================================================
        # SUBSCRIPTION CHECK
        # =================================================

        check_offer_subscription(user, offer.retailer)

        old_name = offer.name

        # =================================================
        # BRANCH VALIDATION
        # =================================================

        try:
            branch = get_offer_branch(
                user=user,
                retailer=offer.retailer,
                request=request,
                existing_offer=offer,
            )
        except ValueError as error:
            return Response(
                {"success": False, "message": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # =================================================
        # SERIALIZER
        # =================================================

        serializer = SalesOfferSerializer(
            offer, data=request.data, partial=partial, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        offer = serializer.save(retailer=offer.retailer, branch=branch)

        # =================================================
        # AUDIT LOG
        # =================================================

        create_audit_log(
            user=user,
            action="update",
            model_name="SalesOffer",
            object_id=offer.id,
            description=(f"Updated Sales Offer from {old_name} to {offer.name}"),
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Sales offer updated successfully.",
                "data": SalesOfferSerializer(offer, context={"request": request}).data,
            },
            status=status.HTTP_200_OK,
        )


# =========================================================
# SOFT DELETE / DEACTIVATE
# =========================================================


class SalesOfferSoftDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, pk):

        offer = get_sales_offer_queryset(request.user, request).filter(id=pk).first()

        if not offer:
            return Response(
                {"success": False, "message": "Sales offer not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not can_manage_offer(request.user, offer):
            return Response(
                {
                    "success": False,
                    "message": "You cannot deactivate this sales offer.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        if not offer.is_active:
            return Response(
                {"success": False, "message": "Offer is already inactive."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        check_offer_subscription(request.user, offer.retailer)

        offer.is_active = False
        offer.deleted_at = timezone.now()

        offer.save(update_fields=["is_active", "deleted_at", "updated_at"])

        create_audit_log(
            user=request.user,
            action="deactivate",
            model_name="SalesOffer",
            object_id=offer.id,
            description=f"Deactivated Sales Offer {offer.name}",
            request=request,
        )

        return Response(
            {"success": True, "message": "Sales offer deactivated successfully."},
            status=status.HTTP_200_OK,
        )


# =========================================================
# ACTIVATE
# =========================================================


class SalesOfferActivateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, pk):

        offer = get_sales_offer_queryset(request.user, request).filter(id=pk).first()

        if not offer:
            return Response(
                {"success": False, "message": "Sales offer not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not can_manage_offer(request.user, offer):
            return Response(
                {"success": False, "message": "You cannot activate this sales offer."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if offer.is_active:
            return Response(
                {"success": False, "message": "Offer is already active."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        check_offer_subscription(request.user, offer.retailer)

        offer.is_active = True
        offer.deleted_at = None

        offer.save(update_fields=["is_active", "deleted_at", "updated_at"])

        create_audit_log(
            user=request.user,
            action="activate",
            model_name="SalesOffer",
            object_id=offer.id,
            description=f"Activated Sales Offer {offer.name}",
            request=request,
        )

        return Response(
            {"success": True, "message": "Sales offer activated successfully."},
            status=status.HTTP_200_OK,
        )


# =========================================================
# HARD DELETE
# =========================================================


class SalesOfferDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def delete(self, request, pk):

        offer = get_sales_offer_queryset(request.user, request).filter(id=pk).first()

        if not offer:
            return Response(
                {"success": False, "message": "Sales offer not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        offer_name = offer.name
        offer_id = offer.id

        try:
            offer.delete()

        except ProtectedError:
            return Response(
                {
                    "success": False,
                    "message": (
                        "This sales offer cannot be permanently deleted "
                        "because it is being used by another record."
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        create_audit_log(
            user=request.user,
            action="delete",
            model_name="SalesOffer",
            object_id=offer_id,
            description=f"Deleted Sales Offer {offer_name}",
            request=request,
        )

        return Response(
            {"success": True, "message": "Sales offer deleted permanently."},
            status=status.HTTP_200_OK,
        )

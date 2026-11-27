from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Count, Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import (
    IsPlatformOwner,
    IsRetailerOwnerOrPlatformOwner,
)

from .models import (
    SupportCategory,
    SupportTicket,
    SupportMessage,
    SupportAttachment,
    PlatformSupportInfo,
    TicketActivity,
)

from .serializers import (
    CreateSupportTicketSerializer,
    ReplySupportTicketSerializer,
    CreateSupportAttachmentSerializer,
    UpdateTicketStatusSerializer,
    SupportTicketListSerializer,
    SupportTicketDetailSerializer,
)

User = get_user_model()


# ==========================================================
# COMMON SUPPORT TICKET ACCESS
# ==========================================================


class SupportTicketAccessMixin:

    def get_accessible_tickets(self, user):

        queryset = SupportTicket.objects.select_related(
            "retailer",
            "branch",
            "created_by",
            "assigned_to",
            "category",
        ).prefetch_related(
            "messages__sender",
            "attachments__uploaded_by",
            "activities__user",
        )

        # Platform Owner can access every retailer's tickets.
        if user.is_superuser:
            return queryset

        retailer_id = getattr(user, "retailer_id", None)

        if not retailer_id:
            return queryset.none()

        role = getattr(user, "role", None)

        # Retailer-level administrators.
        if role in ["superadmin", "admin"]:
            queryset = queryset.filter(retailer_id=retailer_id)

        # Branch Admin can access tickets from their own branch.
        elif role == "branch_admin":

            branch_id = getattr(user, "branch_id", None)

            if not branch_id:
                return queryset.none()

            queryset = queryset.filter(
                retailer_id=retailer_id,
                branch_id=branch_id,
            )

        # Other retailer users can access only their own tickets.
        else:

            queryset = queryset.filter(
                retailer_id=retailer_id,
                created_by=user,
            )

        # Private tickets are visible only to their creator
        # on the retailer side. Platform Owner can always see them.
        queryset = queryset.filter(Q(is_private=False) | Q(created_by=user))

        return queryset


# ==========================================================
# CREATE SUPPORT TICKET
# ==========================================================


class CreateSupportTicketView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):

        retailer = getattr(request.user, "retailer", None)

        if not retailer:
            return Response(
                {
                    "success": False,
                    "message": "Your account is not associated with a retailer.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        branch = getattr(request.user, "branch", None)

        serializer = CreateSupportTicketSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        ticket = SupportTicket.objects.create(
            retailer=retailer,
            branch=branch,
            created_by=request.user,
            category=serializer.validated_data.get("category"),
            subject=serializer.validated_data["subject"],
            description=serializer.validated_data["description"],
            priority=serializer.validated_data.get("priority", "medium"),
        )

        TicketActivity.objects.create(
            ticket=ticket,
            user=request.user,
            action="Ticket Created",
            remarks="Support ticket created.",
        )

        return Response(
            {
                "success": True,
                "message": "Ticket created successfully.",
                "data": {
                    "id": ticket.id,
                    "ticket_number": ticket.ticket_number,
                    "status": ticket.status,
                    "priority": ticket.priority,
                },
            },
            status=status.HTTP_201_CREATED,
        )


# ==========================================================
# SUPPORT TICKET LIST
# ==========================================================


class SupportTicketListView(SupportTicketAccessMixin, APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        queryset = self.get_accessible_tickets(request.user).order_by("-created_at")

        serializer = SupportTicketListSerializer(queryset, many=True)

        return Response(
            {
                "success": True,
                "message": "Support tickets retrieved successfully.",
                "count": queryset.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================================
# SUPPORT TICKET DETAIL
# ==========================================================


class SupportTicketDetailView(SupportTicketAccessMixin, APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        ticket = self.get_accessible_tickets(request.user).filter(pk=pk).first()

        if not ticket:
            return Response(
                {"success": False, "message": "Ticket not found or permission denied."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = SupportTicketDetailSerializer(ticket)

        return Response(
            {
                "success": True,
                "message": "Ticket details retrieved successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================================
# REPLY TO SUPPORT TICKET
# ==========================================================


class ReplyTicketView(SupportTicketAccessMixin, APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, pk):

        ticket = self.get_accessible_tickets(request.user).filter(pk=pk).first()

        if not ticket:
            return Response(
                {"success": False, "message": "Ticket not found or permission denied."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if ticket.status == "closed":
            return Response(
                {"success": False, "message": "Cannot reply to a closed ticket."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ReplySupportTicketSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        message = SupportMessage.objects.create(
            ticket=ticket,
            sender=request.user,
            message=serializer.validated_data["message"],
            is_platform_reply=request.user.is_superuser,
        )

        attachment = serializer.validated_data.get("attachment")

        attachment_data = None

        if attachment:

            support_attachment = SupportAttachment.objects.create(
                ticket=ticket, uploaded_by=request.user, file=attachment
            )

            attachment_data = {
                "id": support_attachment.id,
                "file": support_attachment.file.url,
            }

        TicketActivity.objects.create(
            ticket=ticket,
            user=request.user,
            action="Ticket Replied",
            remarks="A new reply was added.",
        )

        return Response(
            {
                "success": True,
                "message": "Reply added successfully.",
                "data": {
                    "message_id": message.id,
                    "ticket_id": ticket.id,
                    "attachment": attachment_data,
                },
            },
            status=status.HTTP_201_CREATED,
        )


# ==========================================================
# UPLOAD SUPPORT TICKET ATTACHMENT
# ==========================================================


class UploadSupportAttachmentView(SupportTicketAccessMixin, APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, pk):

        ticket = self.get_accessible_tickets(request.user).filter(pk=pk).first()

        if not ticket:
            return Response(
                {"success": False, "message": "Ticket not found or permission denied."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CreateSupportAttachmentSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        attachment = SupportAttachment.objects.create(
            ticket=ticket,
            uploaded_by=request.user,
            file=serializer.validated_data["file"],
        )

        TicketActivity.objects.create(
            ticket=ticket,
            user=request.user,
            action="Attachment Uploaded",
            remarks="A support attachment was uploaded.",
        )

        return Response(
            {
                "success": True,
                "message": "Attachment uploaded successfully.",
                "data": {
                    "id": attachment.id,
                    "ticket_id": ticket.id,
                    "file": attachment.file.url,
                    "uploaded_at": attachment.uploaded_at,
                },
            },
            status=status.HTTP_201_CREATED,
        )


# ==========================================================
# UPDATE SUPPORT TICKET STATUS
# ==========================================================


class UpdateTicketStatusView(SupportTicketAccessMixin, APIView):

    permission_classes = [IsAuthenticated, IsRetailerOwnerOrPlatformOwner]

    @transaction.atomic
    def patch(self, request, pk):

        ticket = self.get_accessible_tickets(request.user).filter(pk=pk).first()

        if not ticket:
            return Response(
                {"success": False, "message": "Ticket not found or permission denied."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = UpdateTicketStatusSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        old_status = ticket.status
        new_status = serializer.validated_data["status"]

        if old_status == new_status:
            return Response(
                {
                    "success": True,
                    "message": "Ticket already has this status.",
                    "data": {"status": ticket.status},
                },
                status=status.HTTP_200_OK,
            )

        ticket.status = new_status

        ticket.save(update_fields=["status", "resolved_at", "updated_at"])

        TicketActivity.objects.create(
            ticket=ticket,
            user=request.user,
            action=f"Status changed from {old_status} to {new_status}",
            remarks=serializer.validated_data.get("remarks"),
        )

        return Response(
            {
                "success": True,
                "message": "Ticket status updated successfully.",
                "data": {
                    "ticket_id": ticket.id,
                    "old_status": old_status,
                    "new_status": ticket.status,
                    "resolved_at": ticket.resolved_at,
                },
            },
            status=status.HTTP_200_OK,
        )


# ==========================================================
# SUPPORT DASHBOARD
# ==========================================================


class SupportDashboardView(APIView):

    permission_classes = [IsAuthenticated, IsPlatformOwner]

    def get(self, request):

        ticket_counts = SupportTicket.objects.aggregate(
            total_tickets=Count("id"),
            open_tickets=Count("id", filter=Q(status="open")),
            in_progress_tickets=Count("id", filter=Q(status="in_progress")),
            resolved_tickets=Count("id", filter=Q(status="resolved")),
            closed_tickets=Count("id", filter=Q(status="closed")),
        )

        return Response(
            {
                "success": True,
                "message": "Support dashboard retrieved successfully.",
                "data": ticket_counts,
            },
            status=status.HTTP_200_OK,
        )

from django.db import transaction
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.permissions import (
    IsPlatformOwner,
    IsRetailerOwnerOrPlatformOwner,
)

from .models import (
    SupportTicket,
    SupportMessage,
    SupportAttachment,
    TicketActivity,
)

from .serializers import (
    CreateSupportTicketSerializer,
    ReplySupportTicketSerializer,
    UpdateTicketStatusSerializer,
    AssignTicketSerializer,
    SupportTicketSerializer,
    SupportTicketListSerializer,
    SupportTicketDetailSerializer,
)

class CreateSupportTicketView(APIView):

    def post(self, request):

        serializer = CreateSupportTicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ticket = SupportTicket.objects.create(
            ticket_number=f"TKT-{timezone.now().strftime('%Y%m%d%H%M%S')}",
            retailer=request.user.retailer,
            branch=request.user.branch,
            created_by=request.user,
            category=serializer.validated_data.get(
                "category"
            ),
            subject=serializer.validated_data["subject"],
            description=serializer.validated_data["description"],
            priority=serializer.validated_data.get(
                "priority",
                "medium"
            ),
        )

        TicketActivity.objects.create(
            ticket=ticket,
            user=request.user,
            action="Ticket Created"
        )

        return Response(
            {
                "success": True,
                "message": "Ticket created successfully",
                "ticket_id": ticket.id,
                "ticket_number": ticket.ticket_number
            },
            status=status.HTTP_201_CREATED
        )
    
class SupportTicketListView(APIView):

    def get(self, request):

        if request.user.is_superuser:

            queryset = SupportTicket.objects.all()

        elif request.user.role == "superadmin":

            queryset = SupportTicket.objects.filter(
                retailer=request.user.retailer
            )

        else:

            queryset = SupportTicket.objects.filter(
                created_by=request.user
            )

        serializer = SupportTicketListSerializer(
            queryset,
            many=True
        )

        return Response(
            {
                "success": True,
                "count": queryset.count(),
                "data": serializer.data
            }
        )
    
class SupportTicketDetailView(APIView):

    def get(self, request, pk):

        try:

            ticket = SupportTicket.objects.get(
                pk=pk
            )

        except SupportTicket.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Ticket not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if not request.user.is_superuser:

            if request.user.role == "superadmin":

                if (
                    ticket.retailer !=
                    request.user.retailer
                ):
                    return Response(
                        {
                            "success": False,
                            "message": "Permission denied"
                        },
                        status=status.HTTP_403_FORBIDDEN
                    )

            elif ticket.created_by != request.user:

                return Response(
                    {
                        "success": False,
                        "message": "Permission denied"
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

        serializer = SupportTicketDetailSerializer(
            ticket
        )

        return Response(
            {
                "success": True,
                "data": serializer.data
            }
        )
    
class ReplyTicketView(APIView):

    def post(self, request, pk):

        serializer = ReplySupportTicketSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:

            ticket = SupportTicket.objects.get(
                pk=pk
            )

        except SupportTicket.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Ticket not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        message = SupportMessage.objects.create(
            ticket=ticket,
            sender=request.user,
            message=serializer.validated_data[
                "message"
            ],
            is_platform_reply=request.user.is_superuser
        )

        attachment = serializer.validated_data.get(
            "attachment"
        )

        if attachment:

            SupportAttachment.objects.create(
                ticket=ticket,
                uploaded_by=request.user,
                file=attachment
            )

        TicketActivity.objects.create(
            ticket=ticket,
            user=request.user,
            action="Ticket Replied"
        )

        return Response(
            {
                "success": True,
                "message": "Reply added successfully"
            }
        )
    
class UpdateTicketStatusView(APIView):

    permission_classes = [
        IsRetailerOwnerOrPlatformOwner
    ]

    def post(self, request, pk):

        serializer = UpdateTicketStatusSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:

            ticket = SupportTicket.objects.get(
                pk=pk
            )

        except SupportTicket.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Ticket not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        ticket.status = serializer.validated_data[
            "status"
        ]

        if ticket.status == "resolved":

            ticket.resolved_at = timezone.now()

        ticket.save()

        TicketActivity.objects.create(
            ticket=ticket,
            user=request.user,
            action=f"Status changed to {ticket.status}",
            remarks=serializer.validated_data.get(
                "remarks"
            )
        )

        return Response(
            {
                "success": True,
                "message": "Status updated successfully"
            }
        )
    
class SupportDashboardView(APIView):

    permission_classes = [IsPlatformOwner]

    def get(self, request):

        return Response(
            {
                "total_tickets":SupportTicket.objects.count(),
                "open_tickets":SupportTicket.objects.filter(status="open").count(),
                "in_progress_tickets":SupportTicket.objects.filter(status="in_progress").count(),
                "resolved_tickets":SupportTicket.objects.filter(status="resolved").count(),
                "closed_tickets":SupportTicket.objects.filter(status="closed").count(),
            }
        )
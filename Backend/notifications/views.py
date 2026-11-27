from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError

from notifications.models import Notification
from notifications.serializers import NotificationSerializer

from notifications.services import (
    get_user_notifications,
    get_unread_notification_count,
    mark_notification_as_read,
    mark_all_notifications_as_read,
    delete_notification,
)

# =====================================================
# NOTIFICATION LIST VIEW
# =====================================================


class NotificationListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        notifications = get_user_notifications(request.user)

        serializer = NotificationSerializer(
            notifications,
            many=True,
        )

        return Response(
            {
                "success": True,
                "message": "Notifications retrieved successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# =====================================================
# NOTIFICATION DETAIL VIEW
# =====================================================


class NotificationDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        notification = Notification.objects.filter(
            id=pk,
            recipient=request.user,
        ).first()

        if notification is None:
            raise NotFound("Notification not found.")

        serializer = NotificationSerializer(notification)

        return Response(
            {
                "success": True,
                "message": "Notification retrieved successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# =====================================================
# UNREAD NOTIFICATION COUNT VIEW
# =====================================================


class UnreadNotificationCountView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        count = get_unread_notification_count(request.user)

        return Response(
            {
                "success": True,
                "message": "Unread notification count retrieved successfully.",
                "data": {
                    "unread_count": count,
                },
            },
            status=status.HTTP_200_OK,
        )


# =====================================================
# MARK SINGLE NOTIFICATION AS READ
# =====================================================


class MarkNotificationReadView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):

        try:
            notification = mark_notification_as_read(
                notification_id=pk,
                user=request.user,
            )

        except DjangoValidationError as exc:
            raise ValidationError(exc.messages)

        serializer = NotificationSerializer(notification)

        return Response(
            {
                "success": True,
                "message": "Notification marked as read successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# =====================================================
# MARK ALL NOTIFICATIONS AS READ
# =====================================================


class MarkAllNotificationsReadView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request):

        updated_count = mark_all_notifications_as_read(request.user)

        return Response(
            {
                "success": True,
                "message": "All notifications marked as read successfully.",
                "data": {
                    "updated_count": updated_count,
                },
            },
            status=status.HTTP_200_OK,
        )


# =====================================================
# DELETE NOTIFICATION VIEW
# =====================================================


class NotificationDeleteView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        try:
            delete_notification(
                notification_id=pk,
                user=request.user,
            )

        except DjangoValidationError as exc:
            raise ValidationError(exc.messages)

        return Response(
            {
                "success": True,
                "message": "Notification deleted successfully.",
                "data": None,
            },
            status=status.HTTP_200_OK,
        )

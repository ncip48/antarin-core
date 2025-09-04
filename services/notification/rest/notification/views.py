# notification/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.db import transaction

from notification.models import Notification, NotificationRecipient
from fcm.utils import notify_users

from .serializers import NotificationSerializer

User = get_user_model()


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all().order_by("-created_at")
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Custom create to handle `type=all|users` and recipients.
        Payload example:
        {
            "title": "New update",
            "body": "Version 2.0 is live!",
            "data": {"screen": "updates"},
            "type": "users",   # or "all"
            "users": ["subid1", "subid2"],  # required if type=users
            "force_popup": true
        }
        """
        title = request.data.get("title")
        body = request.data.get("body")
        data = request.data.get("data", {})
        notif_type = request.data.get("type", "all")
        users = request.data.get("users", [])
        force_popup = request.data.get("force_popup", False)

        if not title or not body:
            return Response(
                {"detail": "Both 'title' and 'body' are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            notification = Notification.objects.create(
                title=title, body=body, data=data, force_popup=force_popup
            )

            recipients = []
            if notif_type == "all":
                all_users = User.objects.all()
                recipients = [
                    NotificationRecipient(notification=notification, user=u)
                    for u in all_users
                ]
            elif notif_type == "users":
                if not users:
                    return Response(
                        {"detail": "'users' must be provided when type='users'."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                target_users = User.objects.filter(subid__in=users)
                recipients = [
                    NotificationRecipient(notification=notification, user=u)
                    for u in target_users
                ]
            else:
                return Response(
                    {"detail": "'type' must be either 'all' or 'users'."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            NotificationRecipient.objects.bulk_create(recipients)
 
            if notif_type == "all":
                notify_users(User.objects.all(), title, body, data=data, force_popup=force_popup)
            elif notif_type == "users":
                notify_users(target_users, title, body, data=data, force_popup=force_popup)

        serializer = self.get_serializer(notification)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"], url_path="me")
    def my_notifications(self, request):
        """
        Return notifications for the authenticated user.
        GET /api/notifications/me/
        """
        user = request.user
        recipient_qs = NotificationRecipient.objects.filter(user=user).select_related("notification")
        notifications = [r.notification for r in recipient_qs]

        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["post"], url_path="resend")
    def resend_notification(self, request, pk=None):
        """
        Resend a notification if it was created with force_popup=True.
        POST /api/notifications/{subid}/resend/
        """
        try:
            notification = self.get_queryset().get(subid=pk)
        except Notification.DoesNotExist:
            return Response(
                {"detail": "Notification not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # find recipients
        recipients = NotificationRecipient.objects.filter(notification=notification)
        users = [r.user for r in recipients]

        if not users:
            return Response(
                {"detail": "No recipients found for this notification."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # re-send push notification
        notify_users(
            users,
            notification.title,
            notification.body,
            data=notification.data,
            force_popup=notification.force_popup,
        )

        return Response(
            {"detail": f"Notification {notification.id} resent to {len(users)} recipients."},
            status=status.HTTP_200_OK,
        )
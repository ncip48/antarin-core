from django.db import models
from core.models import get_subid_model
from django.conf import settings
from chat.models.chat import Chat
from notification.models.notification import Notification

class NotificationRecipient(get_subid_model()):
    """
    Users that are part of a notification.
    """
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name="notifications")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("notification", "user")  # prevent duplicate participants

    def __str__(self):
        return f"{self.user} in {self.notification}"
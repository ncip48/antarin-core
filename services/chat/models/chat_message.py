from django.db import models
from django.conf import settings
from booking.models.trip import Trip

class ChatMessage(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="chat_messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]

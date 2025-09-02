from django.db import models
from core.models import get_subid_model
from django.conf import settings
from chat.models.chat import Chat

class ChatParticipant(get_subid_model()):
    """
    Users that are part of a chat.
    """
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="participants")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    last_read_at = models.DateTimeField(blank=True, null=True)  # track read receipts if needed

    class Meta:
        unique_together = ("chat", "user")  # prevent duplicate participants

    def __str__(self):
        return f"{self.user} in {self.chat}"
from django.db import models
from core.models import get_subid_model


class Chat(get_subid_model()):
    """
    Represents a conversation (could be 1-to-1 or group chat).
    """
    name = models.CharField(max_length=255, blank=True, null=True)  # optional for group chats
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or f"Chat {self.id}"
from django.db import models
from django.conf import settings
from core.models import get_subid_model
from chat.models.chat import Chat
from chat.models.chat_message import ChatMessage

class ChatAttachment(get_subid_model()):
    """
    Stores file attachments for a chat message.
    """
    message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to='attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for message {self.message.subid}"
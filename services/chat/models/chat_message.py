from django.db import models
from django.conf import settings
from core.models import get_subid_model
from chat.models.chat import Chat

class ChatMessage(get_subid_model()):
    """
    Messages inside a chat.
    """
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    
    # +++ ADD THIS FIELD FOR REPLIES +++
    reply_to = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='replies'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]
        
    def __str__(self):
        return f"{self.sender} ({self.created_at}): {self.message[:50]}"

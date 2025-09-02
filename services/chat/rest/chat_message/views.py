from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from chat.models import ChatMessage
from .serializers import ChatMessageSerializer

class ChatMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        subid = self.kwargs.get("subid")
        return ChatMessage.objects.filter(chat__subid=subid)

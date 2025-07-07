from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from chat.models import ChatMessage
from .serializers import ChatMessageSerializer

class ChatMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        booking_id = self.request.query_params.get("booking_id")
        return ChatMessage.objects.filter(booking_id=booking_id)

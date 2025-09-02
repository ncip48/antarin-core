from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from chat.models import Chat
from .serializers import ChatSerializer

class ChatViewSet(viewsets.ModelViewSet):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Chat.objects.filter(participants__user=user)

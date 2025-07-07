from rest_framework import serializers
from chat.models import ChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ["id", "booking", "sender", "message", "timestamp"]

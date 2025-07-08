from rest_framework import serializers
from chat.models import ChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    is_mine = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ["id", "trip", "sender", "message", "created_at", "is_mine"]

    def get_is_mine(self, obj):
        request = self.context.get('request', None)
        if request and hasattr(request, 'user'):
            return obj.sender == request.user
        return False

from rest_framework import serializers
from django.contrib.auth import get_user_model
from chat.models import Chat, ChatParticipant
from authn.rest.auth.serializers import UserSerializer

User = get_user_model()


class ChatParticipantSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ChatParticipant
        fields = ["subid", "user", "joined_at"]


class ChatSerializer(serializers.ModelSerializer):
    opponents = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ["subid", "name", "created_at", "opponents"]

    def get_opponents(self, obj):
        """Return all participants except the logged-in user"""
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return ChatParticipantSerializer(obj.participants.all(), many=True).data

        # Exclude the current user
        opponents = obj.participants.exclude(user=request.user)
        return ChatParticipantSerializer(opponents, many=True, context=self.context).data

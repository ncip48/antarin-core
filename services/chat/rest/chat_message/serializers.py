from rest_framework import serializers
from chat.models import ChatMessage
from authn.rest.auth.serializers import UserSerializer
from chat.models.chat_attachment import ChatAttachment

class ChatAttachmentSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = ChatAttachment
        fields = ["subid", "url", "uploaded_at"]

    def get_url(self, obj):
        try:
            return obj.file.url   # when file is a real FileField
        except Exception:
            return str(obj.file)  # fallback (string path)

class ChatMessageSerializer(serializers.ModelSerializer):
    is_mine = serializers.SerializerMethodField(read_only=True)
    sender = UserSerializer(read_only=True)

    # optional: show minimal info about the replied message
    reply_to = serializers.SerializerMethodField()
    
    # nested attachments
    attachments = ChatAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = ChatMessage
        fields = [
            "subid",
            "sender",
            "message",
            "created_at",
            "is_mine",
            "reply_to",  # <- nested preview
            "attachments",
        ]

    def get_is_mine(self, obj):
        request = self.context.get("request", None)
        if request and hasattr(request, "user"):
            return obj.sender == request.user
        return False

    def get_reply_to(self, obj):
        if obj.reply_to:
            sender = UserSerializer(obj.reply_to.sender).data
            return {
                "subid": obj.reply_to.subid,
                "message": obj.reply_to.message[:50],  # preview first 50 chars
                "sender": sender,
                "created_at": obj.reply_to.created_at.isoformat(),
            }
        return None
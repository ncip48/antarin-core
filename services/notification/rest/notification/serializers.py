# notification/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from notification.models import Notification, NotificationRecipient

User = get_user_model()

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["subid", "title", "body", "data", "force_popup", "created_at"]


class NotificationRecipientSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # or a nested serializer if you want user details
    notification = NotificationSerializer(read_only=True)

    class Meta:
        model = NotificationRecipient
        fields = ["subid", "notification", "user"]
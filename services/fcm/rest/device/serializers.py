from rest_framework import serializers
from fcm.models.fcm_device import FCMDevice

class FCMDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMDevice
        fields = ["token"]
        
    def create(self, validated_data):
        user = self.context["request"].user
        token = validated_data.get("token")

        # upsert by token
        device, _ = FCMDevice.objects.update_or_create(
            token=token,
            defaults={**validated_data, "user": user},
        )
        return device

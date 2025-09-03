from rest_framework import serializers
from fcm.models.fcm_device import FCMDevice

class FCMDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMDevice
        fields = ["token"]

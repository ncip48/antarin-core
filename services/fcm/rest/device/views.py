from rest_framework import generics, permissions
from fcm.rest.device.serializers import FCMDeviceSerializer

class RegisterFCMDeviceView(generics.CreateAPIView):
    serializer_class = FCMDeviceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

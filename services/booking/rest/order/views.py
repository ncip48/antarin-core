from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import TripCreateSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class TripOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TripCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        trip = serializer.save(customer=request.user)

        # Broadcast ke driver yang sedang online
        async_to_sync(get_channel_layer().group_send)(
            "drivers_online",
            {
                "type": "new_order",
                "message": {
                    "order_id": trip.id,
                    "pickup": {
                        "lat": trip.pickup_point.y,
                        "lng": trip.pickup_point.x,
                    },
                    "destination": {
                        "lat": trip.destination_point.y if trip.destination_point else None,
                        "lng": trip.destination_point.x if trip.destination_point else None,
                    },
                },
            }
        )

        return Response({"message": "Trip requested", "trip_id": trip.id})

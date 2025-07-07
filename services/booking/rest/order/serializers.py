from rest_framework import serializers
from django.contrib.gis.geos import Point
from booking.models import Trip

class TripCreateSerializer(serializers.ModelSerializer):
    # Input dalam bentuk lat/lng
    pickup_lat = serializers.FloatField(write_only=True)
    pickup_lng = serializers.FloatField(write_only=True)
    destination_lat = serializers.FloatField(write_only=True, required=False)
    destination_lng = serializers.FloatField(write_only=True, required=False)

    class Meta:
        model = Trip
        fields = [
            "pickup_lat", "pickup_lng",
            "destination_lat", "destination_lng"
        ]

    def create(self, validated_data):
        pickup_point = Point(validated_data.pop("pickup_lng"), validated_data.pop("pickup_lat"))
        dest_lat = validated_data.pop("destination_lat", None)
        dest_lng = validated_data.pop("destination_lng", None)
        destination_point = Point(dest_lng, dest_lat) if dest_lat is not None and dest_lng is not None else None

        return Trip.objects.create(
            pickup_point=pickup_point,
            destination_point=destination_point,
            **validated_data
        )

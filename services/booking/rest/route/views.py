# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.gis.geos import LineString
from booking.models.trip import Trip
from booking.utils import find_real_road_route

class TripRouteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        trip_id = request.query_params.get("trip_id")
        if not trip_id:
            return Response({"detail": "Missing trip_id parameter"}, status=400)

        try:
            trip = Trip.objects.get(id=trip_id)
        except Trip.DoesNotExist:
            return Response({"detail": "Trip not found"}, status=404)

        # Ensure destination_point is filled
        if not trip.destination_point:
            return Response({"detail": "Trip does not have a destination_point yet"}, status=400)

        # Get route as list of (lat, lon)
        route_coords = find_real_road_route(trip.pickup_point, trip.destination_point)

        # Convert to GeoJSON LineString
        line = LineString([(lon, lat) for lat, lon in route_coords])  # GeoJSON uses lon, lat
        geojson = line.geojson  # as JSON string
        import json
        geojson = json.loads(geojson)

        return Response({
            "trip_id": trip.id,
            "route": geojson
        })

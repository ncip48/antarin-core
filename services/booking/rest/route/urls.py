from django.urls import path
from .views import TripRouteView

urlpatterns = [
    path("routes/", TripRouteView.as_view(), name="trip-route"),
]

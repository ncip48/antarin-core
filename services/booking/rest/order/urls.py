from django.urls import path
from .views import TripOrderView

urlpatterns = [
    path("orders/", TripOrderView.as_view(), name="trip-order"),
]

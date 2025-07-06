from django.urls import re_path
from .consumers import DriverConsumer, CustomerConsumer

websocket_urlpatterns = [
    re_path(r"ws/driver/$", DriverConsumer.as_asgi()),
    re_path(r"ws/customer/$", CustomerConsumer.as_asgi()),
]

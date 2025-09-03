from django.contrib import admin
from django.urls import path, include
from .device import urls as device_urls

urlpatterns = [
    path("fcm/", include(device_urls)),
]

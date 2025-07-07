from django.contrib import admin
from django.urls import path, include
from .order import urls as order_urls

urlpatterns = [
    path("order/", include(order_urls)),
]

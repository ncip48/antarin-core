from django.contrib import admin
from django.urls import path, include
from .chat import urls as chat_urls

urlpatterns = [
    path("chat/", include(chat_urls)),
]

from django.contrib import admin
from django.urls import path, include
from .chat import urls as chat_urls
from .chat_message import urls as chat_message_urls

urlpatterns = [
    path("chat/", include(chat_message_urls)),
    path("chat/", include(chat_urls)),
]

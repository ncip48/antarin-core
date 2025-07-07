"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from django.conf import settings
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from booking.routing import websocket_urlpatterns as booking_ws
from chat.routing import websocket_urlpatterns as chat_ws

all_websocket_urlpatterns = booking_ws + chat_ws

django_asgi_app = get_asgi_application()

if settings.DEBUG:
    django_asgi_app = ASGIStaticFilesHandler(django_asgi_app)

application = ProtocolTypeRouter({
    # Untuk permintaan HTTP biasa
    "http": django_asgi_app,

    # Untuk koneksi WebSocket
    "websocket": AuthMiddlewareStack(
        URLRouter(
            all_websocket_urlpatterns
        )
    ),
})


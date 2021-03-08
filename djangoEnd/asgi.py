"""
ASGI config for djangoEnd project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.http import AsgiHandler
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

from djangoEnd.movie.routingWBsocket import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

application = ProtocolTypeRouter({
    'http': AsgiHandler(),
    'websocket': AuthMiddlewareStack(URLRouter(websocket_urlpatterns))

})
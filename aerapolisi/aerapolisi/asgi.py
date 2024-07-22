"""
ASGI config for aerapolisi project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
import main.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aerapolisi.settings')



application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket':AuthMiddlewareStack(
            URLRouter(
                main.routing.websocket_urlpatterns
            )
        )
})

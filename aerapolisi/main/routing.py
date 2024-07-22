from django.urls import re_path
from .consumers import NotificationConsumer

from chat_rooms.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/((?P<room_name>\w+)/$)', ChatConsumer.as_asgi()),
    re_path(r'ws/socket-server/(?P<room_name>\w+)/$', NotificationConsumer.as_asgi()),
]

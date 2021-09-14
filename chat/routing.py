from django.urls import re_path
from channels.routing import URLRouter

from .consumer import ChatConsumer

chat_websocket_urlpatterns = URLRouter(
    [
        re_path(r'ws/chat/(?P<username>\w+)/$', ChatConsumer.as_asgi()),
    ]
)

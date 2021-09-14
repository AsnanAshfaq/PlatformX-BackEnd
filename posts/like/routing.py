from django.urls import re_path, path
from channels.routing import URLRouter

from .consumer import LikeConsumer

like_websocket_urlpatterns = URLRouter(
    [
        re_path(r'ws/chat/(?P<username>\w+)/$', LikeConsumer.as_asgi()),
        # path('ws/like/<uuid:post_id>/<str:username>/', LikeConsumer.as_asgi()),
    ]
)

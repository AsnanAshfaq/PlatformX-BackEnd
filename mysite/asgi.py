"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from django.urls import re_path, path
from channels.routing import ProtocolTypeRouter, URLRouter
from .token import TokenAuthMiddlewareStack
from posts.like.consumer import LikeConsumer
from chat.consumer import ChatConsumer
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Just HTTP for now. (We can add other protocols later.)
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('ws/chat/<str:sender_username>/<str:receiver_username>/', ChatConsumer.as_asgi()),
            path('ws/like/<str:post_id>/<str:username>/', LikeConsumer.as_asgi()),
        ]
        )
    )
})

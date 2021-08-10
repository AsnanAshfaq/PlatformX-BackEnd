from channels.auth import AuthMiddlewareStack
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async


@database_sync_to_async
def get_user_for_token(token_key):
    try:
        jwt_object = JWTAuthentication()
        validated_token = jwt_object.get_validated_token(token_key)
        user = jwt_object.get_user(validated_token)
        return user
    except Token.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        if headers.get(b'authorization'):
            auth = headers.get(b'authorization')
            try:
                token_name, token_key = auth.decode().split()
                if token_name == 'Bearer':
                    user = await get_user_for_token(token_key=token_key)
                    scope['user'] = user
            except:
                scope['user'] = AnonymousUser()
        return await self.app(scope, receive, send)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))

import re

from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from jwt import decode as jwt_decode
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from bSocial import settings


@database_sync_to_async
def get_user(token_key):
    try:
        print(token_key)
        decoded_data = jwt_decode(token_key, settings.SECRET_KEY, algorithms=["HS256"])

        # Will return a dictionary like -
        # {
        #     "token_type": "access",
        #     "exp": 1568770772,
        #     "jti": "5c15e80d65b04c20ad34d77b6703251b",
        #     "user_id": 6
        # }

        # Get the user using ID
        user = get_user_model().objects.get(id=decoded_data["user_id"])
        return user
    except (InvalidToken, TokenError) as e:
        # Token is invalid
        print(e)
        return AnonymousUser()


class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    see:
    https://channels.readthedocs.io/en/latest/topics/authentication.html#custom-authentication
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return TokenAuthMiddlewareInstance(scope, self)


class TokenAuthMiddlewareInstance:
    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner

    async def __call__(self, receive, send):
        close_old_connections()
        headers = dict(self.scope["headers"])
        print(headers[b"cookie"])
        if b"authorization" in headers[b"cookie"]:
            print('still good here')
            cookies = headers[b"cookie"].decode()
            token_key = re.search("authorization=(.*)(; )?", cookies).group(1)
            token = token_key.split(';', 1)[0]
            if token_key:
                self.scope["user"] = await get_user(token)

        inner = self.inner(self.scope)
        return await inner(receive, send)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
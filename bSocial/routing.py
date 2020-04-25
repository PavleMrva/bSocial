from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.conf.urls import url
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from bSocial.channelsmiddleware import TokenAuthMiddleware
from main.consumers import PostConsumer
from django.urls import path

# application = ProtocolTypeRouter({
#     # Empty for now (http->django views is added by default)
#     'websocket': AllowedHostsOriginValidator(
#         AuthMiddlewareStack(
#             URLRouter(
#                 [
#                     url('', PostConsumer)
#                 ]
#             )
#         )
#     )
# })

application = ProtocolTypeRouter({
    "websocket": AllowedHostsOriginValidator(
        TokenAuthMiddleware(
            URLRouter([
                path("notifications/", PostConsumer),
            ])
        )
    )
})



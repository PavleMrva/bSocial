from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.conf.urls import url
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from main.consumers import PostConsumer
from django.urls import path
from main.consumers import NoseyConsumer

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
    "websocket": URLRouter([
        path("notifications/", NoseyConsumer),
    ])
})

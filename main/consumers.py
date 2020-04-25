import asyncio
import json

import channels
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from pyasn1.debug import scope

from .models import Post, Comment

# class PostConsumer(AsyncConsumer):
#     async def websocket_connect(self, event):
#         print("connected", event)
#         await self.send({
#             "type": "websocket.accept",
#         })
#         me = self.scope['user']
#         print(me)
#         obj = await self.get_post(me)
#         print(obj)
#         await self.send({
#             "type": "websocket.send",
#             "text": "Hello World"
#         })
#
#     async def websocket_receive(self, event):
#         print("receive", event)
#
#     async def websocket_disconnect(self, event):
#         print("disconnect", event)
#
#     @database_sync_to_async
#     def get_post(self, user):
#         return user

class PostConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("notification", self.channel_name)
        print(f"Added {self.channel_name} channel to notify")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notification", self.channel_name)
        print(f"Removed {self.channel_name} channel to notify")

    async def post_notif(self, event):
        post_user = event['user_id']
        curr_user = self.scope['user']
        event['current_user_id'] = curr_user.id
        if post_user != curr_user.id:
            await self.send_json(event)

        print(f"Got message {event} at {self.channel_name}")

    async def following_notif(self, event):
        curr_user = self.scope['user']
        if event['following'] == curr_user.username:
            await self.send_json(event)

        print(f"Got message {event} at {self.channel_name}")
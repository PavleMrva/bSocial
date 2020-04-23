import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Post, Comment

class PostConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({
            "type": "websocket.accept",
        })
        me = self.scope['user']
        print(me)
        obj = await self.get_post(me)
        print(obj)
        await self.send({
            "type": "websocket.send",
            "text": "Hello World"
        })

    async def websocket_receive(self, event):
        print("receive", event)

    async def websocket_disconnect(self, event):
        print("disconnect", event)

    @database_sync_to_async
    def get_post(self, user):
        return user
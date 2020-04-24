from django_rq import job

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@job
def long_running():
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "gossip", {"type": "post.notif",
                   "event": "New Post wololo",
                   "username": 'pavle'})
    pass
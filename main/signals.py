from django_rq import job

from .models import Post
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@job
def post_notification(instance):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "post", {"type": "post.notif",
                 "event": f"{instance.user.username} has created a new post",
                 "username": instance.text})

@receiver(post_save, sender=Post)
def announce_new_post(sender, instance, created, **kwargs):
    if created:
        post_notification.delay(instance)
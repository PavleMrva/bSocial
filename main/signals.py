from django_rq import job

from .models import Post, UserFollowing
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


# @job
# def post_notification(instance):
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         "notification", {"type": "post.notif",
#                          "event": "New Post",
#                          "user_id": instance.user.id,
#                          "post_text": instance.text,
#                          "username": instance.user.username})
#

@job
def following_notification(instance):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notification", {"type": "following.notif",
                         "event": "New Following",
                         "follower": instance.follower.username,
                         "following": instance.following.username, })


# @receiver(post_save, sender=Post)
# def announce_new_post(sender, instance, created, **kwargs):
#     if created:
#         post_notification.delay(instance)


@receiver(post_save, sender=UserFollowing)
def announce_new_post(sender, instance, created, **kwargs):
    if created:
        following_notification.delay(instance)

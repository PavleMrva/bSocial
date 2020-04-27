from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django_rq import job


@job
def post_notification(instance):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notification", {"type": "post.notif",
                         "event": "New Post",
                         "user_id": instance.user.id,
                         "post_text": instance.text,
                         "username": instance.user.username})


@job
def comment_notification(instance):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notification", {"type": "comment.notif",
                         "event": "New Comment",
                         "post_user_id": instance.post.user.id,
                         "post_text": instance.post.text,
                         "user_id": instance.user.id,
                         "comment_text": instance.text,
                         "username": instance.user.username})


@job
def following_notification(instance):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notification", {"type": "following.notif",
                         "event": "New Following",
                         "follower": instance.follower.username,
                         "following": instance.following.username, })

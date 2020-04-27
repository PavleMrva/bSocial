from .models import Post, UserFollowing, Comment
from django.db.models.signals import post_save
from django.dispatch import receiver
from .jobs import *


@receiver(post_save, sender=Post)
def announce_new_post(sender, instance, created, **kwargs):
    if created:
        post_notification.delay(instance)


@receiver(post_save, sender=UserFollowing)
def announce_new_following(sender, instance, created, **kwargs):
    if created:
        following_notification.delay(instance) \


@receiver(post_save, sender=Comment)
def announce_new_comment(sender, instance, created, **kwargs):
    if created:
        comment_notification.delay(instance)

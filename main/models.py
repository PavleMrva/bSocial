from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_public = models.BooleanField(default=False)
    
    def FORMAT(self):
        from django.utils.timesince import timesince
        return timesince(self.created_at)

    def publish(self):
        self.save()

    def __str__(self):
        return self.text


class UserFollowing(models.Model):
    following = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)

    class Meta:
        unique_together = ['follower', 'following']

class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).all()
        return qs

    def filter_by_instance(self, instance):
        obj_id = instance.id
        qs = super(CommentManager, self).filter(post=obj_id)
        return qs

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=True)

    objects = CommentManager()

    def FORMAT(self):
        from django.utils.timesince import timesince
        return timesince(self.created_at)

    def approve(self):
        self.approved_comment = True
        self.save()
        
    def disapprove(self):
        self.approved_comment = False
        self.save()

    def __str__(self):
        return self.text


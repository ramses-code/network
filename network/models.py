from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    post = models.TextField(blank=True)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    timestamp = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, blank=True, related_name='liked_posts')

    def serialize(self):
        return {
            'id': self.id,
            'post': self.post,
            'poster': self.poster.username,
            'timestamp': self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            'likes': self.likes.count()
        }

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='follower')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='followed')

    def serialize(self):
        return {
            'follower': self.follower,
            'followed': self.followed
        }
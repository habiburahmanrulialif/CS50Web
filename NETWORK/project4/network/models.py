from django.contrib.auth.models import AbstractUser
from django.db import models
from django_resized import ResizedImageField
import os
from uuid import uuid4

class User(AbstractUser):
    pass


def path_and_rename(instance, filename):
    upload_to = 'network/static/network/image'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class Post(models.Model):
    post_owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name = "poster")
    post_image = models.ImageField(upload_to=path_and_rename, null=True, blank=True)
    post_text = models.TextField()
    post_time = models.DateTimeField(auto_now_add=True)
    post_like = models.ManyToManyField("User", related_name="post_like", blank=True)

    def like_count(self):
        return self.post_like.all().count()

    def __str__(self):
        return f'{self.post_owner} - {self.id}'
    


class Follow(models.Model):
    account = models.ForeignKey("User", on_delete=models.CASCADE, related_name="follow_account")
    follower = models.ManyToManyField("User", related_name="follower", blank=True)
    following = models.ManyToManyField("User", related_name="following", blank=True)

    def follower_count(self):
        return self.follower.all().count()
    
    def following_count(self):
        return self.following.all().count()
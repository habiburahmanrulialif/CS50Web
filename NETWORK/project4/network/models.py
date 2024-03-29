from django.contrib.auth.models import AbstractUser
from django.db import models
import os
from uuid import uuid4
from django.dispatch import receiver
from django.db.models.signals import post_save

class User(AbstractUser):
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Create Follow instance for the new user
        Follow.objects.get_or_create(account=self)
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
    post_text = models.TextField(null=True, blank=True)
    post_date = models.DateField(auto_now_add=True)
    post_time = models.TimeField(auto_now_add=True)
    post_like = models.ManyToManyField("User", related_name="post_like", blank=True)

    def clean_post_time(self):
        # Remove milliseconds by setting microseconds to zero
        if self.post_time:
            clean = self.post_time.strftime('%H:%M:%S')
            return clean
        return None

    def like_by_user(self, user):
        return self.post_like.filter(pk=user.pk).exists()

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
    
    @classmethod
    def create_follow_for_user(cls, user):
        follow, created = cls.objects.get_or_create(account=user)
        return follow

@receiver(post_save, sender=User)
def create_follow_for_new_user(sender, instance, created, **kwargs):
    if created:
        Follow.objects.get_or_create(account=instance)
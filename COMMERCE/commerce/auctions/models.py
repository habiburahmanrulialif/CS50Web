from django.contrib.auth.models import AbstractUser
from django.db import models
from django_resized import ResizedImageField
from django.db import models
from django.utils import timezone
import os
from uuid import uuid4


class User(AbstractUser):
    pass


def path_and_rename(instance, filename):
    upload_to = 'auctions/static/auctions/image'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class category(models.Model):
    categoryName = models.CharField(max_length=50)

    def __str__(self):
        return self.categoryName


class bid(models.Model):

    bid_amout = models.IntegerField()
    bidder = models.ForeignKey("User", blank=True, null=True, on_delete=models.CASCADE)


class listing(models.Model):
    name = models.CharField(max_length=64)
    desc = models.TextField(default='No Descriptions')
    image = ResizedImageField(size=[1920, 1080], upload_to=path_and_rename)
    # Booleanfield default = true, which mean listing still open. And False when listing closed
    status = models.BooleanField(default=True)
    owner = models.ForeignKey("User", on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey("category", on_delete=models.CASCADE, blank=True, null=True)
    date_post = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    def __str__(self):
        return str(self.name) 

from django.contrib.auth.models import AbstractUser
from django.db import models
from django_resized import ResizedImageField
from django.db import models
from django.utils import timezone
import os
from uuid import uuid4


class User(AbstractUser):
    wishlist = models.ManyToManyField("listing")
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

    bid_amount = models.IntegerField()
    bidder = models.ForeignKey("User", blank=True, null=True, on_delete=models.CASCADE)
    bid_listing = models.ForeignKey("listing", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.bidder}'
    


class listing(models.Model):
    name = models.CharField(max_length=64)
    desc = models.TextField(blank=True, null=True)
    image = ResizedImageField(size=[1920, 1080], upload_to=path_and_rename, null=True, blank=True)
    image_url = models.CharField(max_length=512, blank=True, null=True, default='')
    # Booleanfield default = true, which mean listing still open. And False when listing closed
    status = models.BooleanField(default=True)
    owner = models.ForeignKey("User", on_delete=models.CASCADE, blank=True, null=True, related_name='owner')
    category = models.ForeignKey("category", on_delete=models.CASCADE, blank=True, null=True)
    date_post = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    winner = models.ForeignKey("user", on_delete=models.CASCADE, blank=True, null=True, related_name='winner')
    starting_price = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.name) 


class comment(models.Model):
    commenter = models.ForeignKey("User", on_delete=models.CASCADE)
    comment = models.TextField()
    post_date = models.TimeField(auto_now_add=True)
    comment_listing = models.ForeignKey("listing", on_delete=models.CASCADE)
    comment_listing_id = comment_listing.name

    def __str__(self):
        return f'{self.commenter} - { self.comment_listing}'
    
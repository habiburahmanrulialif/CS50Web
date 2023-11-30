from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class listing(models.Model):
    name = models.CharField(max_length=64)
    price = models.IntegerField()
    desc = models.TextField(default='No Descriptions')
    image = models.ImageField(upload_to=None)
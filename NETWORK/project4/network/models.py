from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post:
    post_owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name = "poster")
    post_image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    post_text = models.TextField()
    post_time = models.DateTimeField(auto_now_add=True)
    post_like = models.ManyToManyField("User", related_name="post like")
    post_like_count = models.IntegerField()

    def serialize(self):
        return {
            "post_id": self.id,
            "post_owner": self.post_owner.username,
            "post_image": self.post_image,
            "post_text" : self.post_text,
            "post_time" : self.post_time.strftime("%b %d %Y, %I:%M %p"),
            "post_like" : [user.username for user in self.post_like],
            "post_like_count" : self.post_like_count
        }


class Follow:
    account = models.ForeignKey("User", on_delete=models.CASCADE, related_name="follow account")
    follower = models.ManyToManyField("User", related_name="follower")
    follower_count = models.IntegerField()
    following = models.ManyToManyField("User", related_name="following")
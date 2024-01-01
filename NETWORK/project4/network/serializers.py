from rest_framework import serializers
from rest_framework.decorators import api_view
from .models import Post, Follow

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields =  ["id", "post_owner", "post_image", "post_text", "post_time", "post_like", "like_count"]


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model : Follow
        fields : ["id", "account", "follower", "following", "follower_count"]
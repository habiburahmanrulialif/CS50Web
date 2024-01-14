from rest_framework import serializers
from .models import Post, Follow

class PostSerializer(serializers.ModelSerializer):
    post_owner = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(source='post_owner.username', read_only=True)
    class Meta:
        model = Post
        fields =  ["id","post_owner", "post_image", "post_text","post_time", "clean_post_time","post_date","post_like","like_count", "username"]


class FollowSerializer(serializers.ModelSerializer):
    account = serializers.PrimaryKeyRelatedField(read_only=True)
    account_name = serializers.CharField(source='account.username', read_only=True)
    class Meta:
        model = Follow
        fields = ["id", "account", "follower", "following", "follower_count", "following_count", "account_name"]
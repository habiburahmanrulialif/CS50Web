from django.contrib import admin
from .models import User, Post, Follow

class PostAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "like_count")

class FollowAdmin(admin.ModelAdmin):
    readonly_fields = ("follower_count", )

admin.site.register(User)
admin.site.register(Post, PostAdmin)
admin.site.register(Follow, FollowAdmin)
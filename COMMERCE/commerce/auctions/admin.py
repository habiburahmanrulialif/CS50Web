from django.contrib import admin
from .models import listing, category, comment, bid, User


class listingAdmin(admin.ModelAdmin):
    readonly_fields = ('id', "date_post")

class commentAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'comment_listing_id')

admin.site.register(listing, listingAdmin)

admin.site.register(category)

admin.site.register(comment, commentAdmin)

admin.site.register(bid)

admin.site.register(User)
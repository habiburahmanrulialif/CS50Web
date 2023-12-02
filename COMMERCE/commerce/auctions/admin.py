from django.contrib import admin
from .models import listing, category


class listingAdmin(admin.ModelAdmin):
    readonly_fields = ('id', "date_post")

admin.site.register(listing, listingAdmin)

admin.site.register(category)
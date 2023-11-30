from django.contrib import admin
from .models import listing


class listingAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(listing, listingAdmin)
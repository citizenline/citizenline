from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Site, SiteProfile


# For models using site to always set current site
class SiteProfileModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.site = Site.objects.get_current()
        obj.save()

admin.site.register(SiteProfile, SiteProfileModelAdmin)
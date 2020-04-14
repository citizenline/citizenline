
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from django.db import models
from django.contrib.sites.managers import CurrentSiteManager
from ckeditor.fields import RichTextField


class SiteProfileManager(CurrentSiteManager):
    def get_query_set(self):
        return super(SiteProfileManager, self).get_query_set()

class SiteProfile(models.Model):
    site = models.OneToOneField(Site, default=1, editable=False, on_delete=models.CASCADE, related_name="siteProfile")
    objects = SiteProfileManager()
    header = RichTextField(_("header"), max_length=20000, blank=True)
    footer = RichTextField(_("footer"), max_length=20000, blank=True)

    class Meta:
        verbose_name = _("site profile")
        verbose_name_plural = _("site profiles")

    def __str__(self):
        return self.site.domain
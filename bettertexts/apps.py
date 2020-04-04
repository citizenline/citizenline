from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete
from django.utils.translation import ugettext_lazy as _


class ImprovetextAppConfig(AppConfig):
    name = "bettertexts"
    verbose_name = _("Better texts")

    def ready(self):
        from .models import UserRating
        from .signals import calculate_ratings

        post_save.connect(calculate_ratings, sender=UserRating)
        post_delete.connect(calculate_ratings, sender=UserRating)

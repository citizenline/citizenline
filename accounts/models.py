from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

User._meta.get_field('email')._unique = True
User._meta.get_field('email')._error_messages = {
            'unique': _("A user with that email address already exists."),
        }

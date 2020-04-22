"""
WSGI config for citizenline project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os, sys

sys.path.append('/opt/bitnami/apps/django/django_projects/citizenline')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "citizenline.settings.bitnami")

application = get_wsgi_application()

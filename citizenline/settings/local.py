from citizenline.settings.base import *  # noqa


INSTALLED_APPS += ("debug_toolbar",)

MIDDLEWARE_CLASSES += ("debug_toolbar.middleware.DebugToolbarMiddleware",)

# The Django Debug Toolbar will only be shown to these client IPs.
INTERNAL_IPS = ("127.0.0.1",)

DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
    "SHOW_TEMPLATE_CONTEXT": True,
    "HIDE_DJANGO_SQL": False,
}

# AUTH_USER_MODEL = 'citizenline_admin.User'

# The cache connection to use for django-multisite.
# Default: 'default'
CACHE_MULTISITE_ALIAS = "default"

# The cache key prefix that django-multisite should use.
# Default: '' (Empty string)
CACHE_MULTISITE_KEY_PREFIX = ""

MULTISITE_FALLBACK = "django.views.generic.base.RedirectView"

MULTISITE_FALLBACK_KWARGS = {"url": "http://www.citizenline.local/", "permanent": False}

# SITE_ID = 1
# SITE_ID = SiteID(default=1)


# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#     }
# }

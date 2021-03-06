from citizenline.settings.base import *  # noqa

DEBUG = False

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

ALLOWED_HOSTS = [".citizenline.nl"]
WWW_HOST = "www.citizenline.nl"

EMAIL_HOST = "localhost"
EMAIL_PORT = 25
EMAIL_USE_TLS = False

# TODO: Setup proper production cache
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#     }
# }

# Use the cached template loader so template is compiled once and read from
# memory instead of reading from disk on each load.
# TEMPLATES[0]['OPTIONS']['loaders'] = [
#    ('django.template.loaders.cached.Loader', [
#        'django.template.loaders.filesystem.Loader',
#        'django.template.loaders.app_directories.Loader',
#    ]),
# ]

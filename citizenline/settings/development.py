from citizenline.settings.base import *  # noqa

DEBUG = True


ALLOWED_HOSTS = [".citizenline.nl", "localhost"]
WWW_HOST = "www-test.citizenline.nl"

EMAIL_HOST = "localhost"
EMAIL_PORT = 25
EMAIL_USE_TLS = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("DATABASE_NAME", "citizenline-dev"),
        "USER": os.getenv("DATABASE_USER", "citizenline-dev"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD", "citizenline-dev"),
        "HOST": os.getenv("DATABASE_HOST", "localhost"),
        "PORT": os.getenv("DATABASE_PORT", "5432"),
    }
}


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

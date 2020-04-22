from citizenline.settings.base import *  # noqa

DEBUG = True


ALLOWED_HOSTS = [".citizenline.nl"]
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

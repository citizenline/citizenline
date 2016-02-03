# Import * her just for DEV environment! Shouldn't do that elsewhere.
from .settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%of1xgdp+8s&b7g+dmr^9=0b!rlg5)imp_$wx8lig-*u%pzq33'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

#LANGUAGE_CODE = 'en-us'
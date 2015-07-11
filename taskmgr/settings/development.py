import os
from .common import *
DEBUG = True

ALLOWED_HOSTS = []


FULL_DOMAIN_NAME = 'http://localhost:8000'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Kuala_Lumpur'

USE_I18N = False

USE_L10N = True

USE_TZ = True


# if os.environ.get('HEROKU_ENV') is not None:
#     STATIC_ROOT = 'staticfiles'

STATIC_ROOT = os.path.join(BASE_DIR, "static", "static_root")



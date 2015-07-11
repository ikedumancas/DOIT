import os
from .common import *
DEBUG = True

ALLOWED_HOSTS = []


FULL_DOMAIN_NAME = 'http://localhost:8000'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'taskmgr_db',                      
        'USER': os.environ.get('DB_UNAME'),
        'PASSWORD': os.environ.get('DB_PWORD'),
        'HOST': 'localhost',
        'PORT': '',
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



import os
from .common import *
DEBUG = True

ALLOWED_HOSTS = []


FULL_DOMAIN_NAME = 'http://localhost:8000'
from .db_settings import DB_NAME, DB_UNAME, DB_PWD, DB_HOST, DB_PORT
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,                      
        'USER': DB_UNAME,
        'PASSWORD': DB_PWD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}
TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Kuala_Lumpur'

USE_I18N = False

USE_L10N = True

USE_TZ = True


if os.environ.get('HEROKU_ENV') is not None:
    STATIC_ROOT = 'staticfiles'

STATIC_ROOT = os.path.join(BASE_DIR, "static", "static_root")



DEBUG = True

ALLOWED_HOSTS = []


FULL_DOMAIN_NAME = 'http://tskmgr.com'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Kuala_Lumpur'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/


if os.environ.get('HEROKU_ENV') is not None:
    STATIC_ROOT = 'staticfiles'
else:
    STATIC_ROOT = os.path.join(BASE_DIR, "static", "static_root")
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static", "static_dirs"),
)


MEDIA_ROOT =  os.path.join(BASE_DIR, "static", "static_dirs")

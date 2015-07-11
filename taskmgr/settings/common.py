import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECRET_KEY = '_*qs=0hyn(2mr_jb0!rci@a+4caq_jzvb85arj)^43i4_(3gw#'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'

LANGUAGE_CODE = 'en-us'


########## MANAGER CONFIGURATION
# Admin and managers for this project. These people receive private site
# alerts.
ADMINS = (
    ('Miguel Ike Dumancas', 'ikedumancas@gmail.com'),
)

MANAGERS = ADMINS
########## END MANAGER CONFIGURATION


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'account',
    'tasks'
)



MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'taskmgr.middleware.TimezoneMiddleware',
)

ROOT_URLCONF = 'taskmgr.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'taskmgr.wsgi.application'
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT =  os.path.join(BASE_DIR, "static", "static_dirs")
CRISPY_TEMPLATE_PACK = 'bootstrap3'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static", "static_dirs"),
)
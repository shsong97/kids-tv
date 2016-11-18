import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# heroku config var settings
# Add config var SECRET_KEY and value
DEFAULT_SECRET_KEY = 'n+g79y=q+bg*)mm_e=_pyl)t0i5x1=iuo8q2g02*mhbke*35jy'
SECRET_KEY = os.environ.get('SECRET_KEY', DEFAULT_SECRET_KEY)
DEBUG = bool(os.environ.get('DEBUG_MODE', ''))

# Application definition

INSTALLED_APPS = (
    'django.contrib.sites', # mail setting
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'kid',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'kids.urls'

WSGI_APPLICATION = 'kids.wsgi.application'

# heroku setting & local default
# Parse database configuration from $DATABASE_URL
import dj_database_url
local_db = 'postgres://kidstv:kidstv@localhost/kidstv'
DATABASES = { 'default' : dj_database_url.config(default=local_db) }

LANGUAGE_CODE = 'ko-KR'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
# gmail setting
SITE_ID = 1

EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_HOST_USER='shsong97@gmail.com'
EMAIL_HOST_PASSWORD='tmdgns1997'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'shsong97@gmail.com'
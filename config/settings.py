from datetime import timedelta
from pathlib import Path
import os

from .mail_info import (
    YANDEX_APP_PASSWORD,
    YANDEX_MAIL_NAME
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-t+rsb(0p)g!xhf%17u5%ajgfm6ogzr0l77ynar6*t*8z21nn=*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'src.routers',

    'src.oauth.apps.OauthConfig',
    'src.Announcements.apps.AnnouncementsConfig',
    'src.Profile',

    'rest_framework',
    'drf_yasg',
    'django_filters',

    'django_celery_beat',
    'django_celery_results',

    'corsheaders',
]

CORS_ALLOW_ALL_ORIGINS = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates', ],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
   'default': {
      'ENGINE': 'django.db.backends.postgresql_psycopg2',
      'NAME': 'fordb',
      'USER': 'admin',
      'PASSWORD': 'admin',
      'HOST': 'localhost',
      'PORT': '5432',
   },
}



# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

"""Additional settings and constants"""

AUTH_USER_MODEL = 'oauth.User'
USER_EMAIL_CONFIRM_ENDPOINT = '/sing-in/email-conformation/'
USER_EMAIL_CONFIRM_ENDPOINT_FULL = USER_EMAIL_CONFIRM_ENDPOINT + '<int:pk>/<str:token>/'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 30,


    'DEFAULT_AUTHENTICATION_CLASSES': (
        'src.oauth.services.backend_auth.AuthBackend',
    ),
    'DEFAULT_PERMISSIONS_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ]

}

"""JTW"""
JWT_AUTH = {
    'JWT_ENCODE_HANDLER':
        'rest_framework_jwt.utils.jwt_encode_handler',
    'JWT_DECODE_HANDLER':
        'rest_framework_jwt.utils.jwt_decode_handler',
    'JWT_PAYLOAD_HANDLER':
        'rest_framework_jwt.utils.jwt_payload_handler',
    'JWT_PAYLOAD_GET_USER_ID_HANDLER':
        'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',
    'JWT_RESPONSE_PAYLOAD_HANDLER':
        'rest_framework_jwt.utils.jwt_response_payload_handler',

    'JWT_SECRET_KEY': 'SECRET_KEY',
    'JWT_GET_USER_SECRET_KEY': None,
    'JWT_PUBLIC_KEY': None,
    'JWT_PRIVATE_KEY': None,
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': timedelta(days=30),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,
    'JWT_ALLOW_REFRESH': False,
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=30),
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_AUTH_COOKIE': None,
}


"""Media files settings"""

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

URL_ANNOUNCEMENT_PICTURES = '<int:pk>/picture/<int:img_num>/'
MAX_MEGABYTE_USER_AVATAR = 2

"""Debug toolbar"""

INTERNAL_IPS = [

]

"""JWT Token"""

ALGORITHM = 'HS256'
ACCES_TOKEN_EXPIRE_MINUTES = 60 * 24


"""Google"""

GOOGLE_CLIENT_ID = '968697474823-irc1afua92ergsnkg3cu1cs3p4sk4v1m.apps.googleusercontent.com'

"""Swagger"""

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
}

"""Mailling from yandex"""

EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = YANDEX_MAIL_NAME
EMAIL_HOST_PASSWORD = YANDEX_APP_PASSWORD
EMAIL_HOST_USER_FULL = EMAIL_HOST_USER + '@yandex.ru'
EMAIL_USE_SSL = True


PROTOCOL = 'http'
DOMEN = 'localhost'
PORT = '8000'
INDEX_URL = f'{PROTOCOL}://{DOMEN}:{PORT}'

API_AND_VERSION = 'api/v1/'
INDEX_URL_API = f'{INDEX_URL}/{API_AND_VERSION}'

EMAIL_CONFORMATION_URL_ENDPOINT = f'email-conformation/<str:token>/'
EMAIL_CONFORMATION_URL = f'{INDEX_URL}sign-in/email-confirm/'


"""Celery + Redis  Settings"""

REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
REDIS_RESULT = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
REDIS_URL = REDIS_RESULT
CELERY_BROKER_URL = REDIS_URL
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60


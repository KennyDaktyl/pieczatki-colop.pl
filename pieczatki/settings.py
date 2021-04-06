import socket
from django.contrib.auth import get_user_model
import django
from pathlib import Path
import os
import sys

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = [
    '*',
]

if socket.gethostname() == "Asus":
    SECURE_SSL_REDIRECT = False
    DEBUG = True
    DOMAIN = "127.0.0.1"
    DatabaseName = "colop_v1"
    SECURE_SSL_REDIRECT = False
else:
    DOMAIN = "pieczatki-colop.pl"
    DatabaseName = "colop_v1"
    DEBUG = False
    SECURE_SSL_REDIRECT = False
    SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
    SESSION_COOKIE_DOMAIN = f".{DOMAIN}"
    SESSION_COOKIE_HTTPONLY = True
    # SESSION_COOKIE_AGE = 10 * 60
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True
    SESSION_SAVE_EVERY_REQUEST = True
    CSRF_COOKIE_DOMAIN = f".{DOMAIN}"
    CSRF_COOKIE_HTTPONLY = True

# Application definition

INSTALLED_APPS = [
    'account.apps.AccountConfig', 'django.contrib.admin',
    'django.contrib.auth', 'django.contrib.contenttypes',
    'django.contrib.sessions', 'django.contrib.messages',
    'django.contrib.staticfiles', 'django.contrib.sites',
    'django.contrib.sitemaps', 'crispy_forms', 'captcha', 'sorl.thumbnail',
    'front', 'products'
]

SITE_ID = 1
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pieczatki.urls'

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
                'django.template.context_processors.media',
                # 'social.apps.django_app.context_processors.backends',
                # 'social.apps.django_app.context_processors.login_redirect',
                # 'social_django.context_processors.backends',  # <--
                # 'social_django.context_processors.login_redirect',  # <--
            ],
        },
    },
]

WSGI_APPLICATION = 'pieczatki.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "NAME": DatabaseName,
        "ENGINE": "django.db.backends.postgresql",
        "USER": os.environ.get('DB_USER'),
        "PASSWORD": os.environ.get('DB_PASSWORD'),
        "HOST": "localhost",
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'pl'
TIME_ZONE = 'Europe/Warsaw'
USE_I18N = True
USE_L10N = True
USE_TZ = False
DATETIME_FORMAT = "Y-m-d H:M:S"
DATE_INPUT_FORMATS = "Y-m-d H:M:S"

STATIC_URL = '/static/'
STATIC_ROOT = "static"
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
STATICFILES_DIRS = (os.path.join(SITE_ROOT, "static/"), )
MEDIA_URL = '/media/'
# MEDIA_URL = f'http://127.0.0.1:8000/static/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

ALLOWED_UPLOAD_IMAGES = ('webp', 'png', 'bmp', 'jpeg', 'jpg')

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend', )

CRISPY_TEMPLATE_PACK = 'uni_form'

RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAP_PUBKEY')
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAP_PRIVKEY')

# THUMBNAIL_COLORSPACE = None
# THUMBNAIL_PRESERVE_FORMAT = True
# THUMBNAIL_QUALITY = 100

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#         'LOCATION': 'cache',
#     }
# }

DJANGORESIZED_DEFAULT_SIZE = [1280, 960]
DJANGORESIZED_DEFAULT_QUALITY = 100
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'WEBP'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {'WEBP': ".webp"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True

# THUMBNAILS = {
#     'METADATA': {
#         'PREFIX': 'thumbs',
#         'BACKEND': 'thumbnails.backends.metadata.RedisBackend',
#         'db': 2,
#         'port': 6379,
#         'host': 'localhost',
#     },
# }

# THUMBNAILS = {
#     'METADATA': {
#         'BACKEND': 'thumbnails.backends.metadata.DatabaseBackend',
#     },
#     'STORAGE': {
#         'BACKEND': 'django.core.files.storage.FileSystemStorage',
#         # You can also use Amazon S3 or any other Django storage backends
#     },
#     'SIZES': {
#         'small': {
#             'PROCESSORS': [{
#                 'PATH': 'thumbnails.processors.resize',
#                 'width': 10,
#                 'height': 10
#             }, {
#                 'PATH': 'thumbnails.processors.crop',
#                 'width': 80,
#                 'height': 80
#             }],
#             'POST_PROCESSORS': [
#                 {
#                     'PATH': 'thumbnails.post_processors.optimize',
#                     'png_command': 'optipng -force -o7 "%(filename)s"',
#                     'jpg_command': 'jpegoptim -f --strip-all "%(filename)s"',
#                 },
#             ],
#         },
#         'large': {
#             'PROCESSORS': [{
#                 'PATH': 'thumbnails.processors.resize',
#                 'width': 20,
#                 'height': 20
#             }, {
#                 'PATH': 'thumbnails.processors.flip',
#                 'direction': 'horizontal'
#             }],
#         }
#     }
# }
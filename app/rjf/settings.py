# -*- coding: utf-8 -*-
"""
Django settings for rjf project.
"""
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from pathlib import Path
import cbs
import dj_database_url

from utils.env_wrapper import Env

# app directory, contains 'rjf' and other apps
BASE_DIR = Path(__file__).resolve().parent
# top directory, contains the entire application
TOP_DIR = BASE_DIR.parent

env = Env()
MODE = env.get('DJANGO_MODE', 'dev').title()


# all of the following must be visible for PyCharm to resolve
STATICFILES_DIRS = [        # where static files are found
    BASE_DIR / 'static',
]
STATICFILES_FINDERS = [
    'npm.finders.NpmFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
STATIC_ROOT = TOP_DIR / 'static'
MEDIA_ROOT = TOP_DIR / 'media'
INSTALLED_APPS = [
    'core',
    'cms_blocks',
    'cms'
]
SECRET_KEY = env.get('DJANGO_SECRET_KEY', 'this is not really a secret key')


# Base app settings

class BaseSettings:

    INSTALLED_APPS = [
        'wagtail.contrib.forms',
        'wagtail.contrib.redirects',
        'wagtail.embeds',
        'wagtail.sites',
        'wagtail.users',
        'wagtail.snippets',
        'wagtail.documents',
        'wagtail.images',
        'wagtail.search',
        'wagtail.admin',
        'wagtail.core',

        'modelcluster',
        'taggit',

        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ] + INSTALLED_APPS

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'wagtail.contrib.redirects.middleware.RedirectMiddleware',
        'django.middleware.cache.FetchFromCacheMiddleware',  # must be last
    ]

    ROOT_URLCONF = 'rjf.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                BASE_DIR / 'templates',
            ],
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

    ASGI_APPLICATION = 'rjf.asgi.application'
    WSGI_APPLICATION = 'rjf.wsgi.application'

    DATABASES = {
        'default': dj_database_url.config('DJANGO_DATABASE_URL', conn_max_age=1800)
    }

    # Redis cache: Pages and session cache
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': env.get('DJANGO_REDIS_URL'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient'
            }
        },
        'sessions': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': env.get('DJANGO_REDIS_URL'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient'
            }
        }
    }
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    SESSION_CACHE_ALIAS = 'sessions'

    MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

    # Password validation
    # https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
    # https://docs.djangoproject.com/en/3.1/topics/i18n/

    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # Static files (CSS, JavaScript, Images)
    STATIC_URL = '/static/'
    STATICFILES_DIRS = STATICFILES_DIRS  # where static files are found
    STATICFILES_FINDERS = STATICFILES_FINDERS

    # ManifestStaticFilesStorage is recommended in production, to prevent outdated
    # Javascript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
    # See https://docs.djangoproject.com/en/3.1/ref/contrib/staticfiles/#manifeststaticfilesstorage
    STATIC_ROOT = STATIC_ROOT
    MEDIA_ROOT = MEDIA_ROOT
    MEDIA_URL = '/media/'

    NPM_ROOT_PATH = BASE_DIR
    NPM_FILE_PATTERNS = {
    }

    # support authentication via username or email
    AUTHENTICATION_BACKENDS = [
        'rjf.auth.EmailOrUsernameAuthBackend',
    ]

    # Message tags
    from django.contrib import messages
    MESSAGE_TAGS = {
        messages.DEBUG: 'alert-info',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
    }

    # Wagtail settings
    WAGTAIL_SITE_NAME = "rjf"
    BASE_URL = 'http://example.com'


class DevSettings(BaseSettings):
    DEBUG = env.bool('DJANGO_DEBUG', default=True)
    ALLOWED_HOSTS = ['*']
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    BASE_URL = 'http://localhost:8000'


class TestSettings(DevSettings):
    pass


class BetaSettings(BaseSettings):
    DEBUG = env.bool('DJANGO_DEBUG', default=False)
    BASE_URL = 'https://beta.rjf.org.au'
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
    ALLOWED_HOSTS = [
        'localhost',
        '127.0.0.1',
        '::1',
        # my_external_ip_address
        # my_domain
        # my_domain_aliases ...
    ]


class ProdSettings(BaseSettings):
    BASE_URL = 'https://rjf.org.au'


cbs.apply(f'{MODE}Settings', globals())

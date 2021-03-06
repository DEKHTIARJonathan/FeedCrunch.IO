#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""
Django settings for application project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import sys
import getenv

from datetime import timedelta

from celery.schedules import crontab

from kombu import Exchange
from kombu import Queue

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test' #Define a variable to know if we are in tests

# ================== We append to the path the function folder containing generic functions

functions_dir = os.path.join(BASE_DIR, 'functions')
sys.path.insert(0, functions_dir)

#################################################################################

STATICFILES_LOCATION = 'static'
STATIC_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'staticfiles')
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

MEDIAFILES_LOCATION = 'media'
MEDIA_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), MEDIAFILES_LOCATION)


def assign_env_value(var_name):
    if var_name in os.environ:
        return getenv.env(var_name)
    else:
        sys.exit(var_name + " is not defined in the environment variables")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECURITY WARNING: don't run with debug turned on in production!


DEBUG = assign_env_value('DEBUG')
SECRET_KEY = assign_env_value('SECRET_KEY')

if DEBUG or TESTING:

    # Simplified static file serving.
    # https://warehouse.python.org/project/whitenoise/
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    STATIC_URL = "/%s/" % STATICFILES_LOCATION

    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

    # Storage URL
    MEDIA_URL = "/%s/" % MEDIAFILES_LOCATION

    # ========== Bypass SSL Certificate Verification ===========
    import ssl
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context

else:

    AWS_HEADERS = {  # see http://developer.yahoo.com/performance/rules.html#expires
        'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
        'Cache-Control': 'max-age=120', #max age in seconds => i.e : 94608000 = 3 years, 3600 = 1 hour, 120 = 2min
    }

    AWS_STORAGE_BUCKET_NAME = 'feedcrunch'
    AWS_ACCESS_KEY_ID = assign_env_value('AWS_USER')
    AWS_SECRET_ACCESS_KEY = assign_env_value('AWS_SECRET_KEY')

    # Tell django-storages that when coming up with the URL for an item in S3 storage, keep
    # it simple - just use this domain plus the path. (If this isn't set, things get complicated).
    # This controls how the `static` template tag from `staticfiles` gets expanded, if you're using it.
    # We also use it in the next setting.
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

    ################################################################################ STATIC FILES ################################################

    # Tell the staticfiles app to use S3Boto storage when writing the collected static files (when you run `collectstatic`).
    STATICFILES_STORAGE = 'application.custom_storages.StaticStorage'
    STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)

    ################################################################################ STATIC FILES ################################################

    # Tell the staticfiles app to use S3Boto storage when serving and uploading media files.
    DEFAULT_FILE_STORAGE = 'application.custom_storages.MediaStorage'
    MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)

#######################################################

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'django_extensions',
    'django_ses',
    'rest_framework',
    'rest_framework.authtoken',
    'encrypted_model_fields',
    'storages',
    'django_celery_monitor',
    'django_celery_beat',
    # 'django_celery_results',
]

LOCAL_APPS = [
    'feedcrunch',
    'feedcrunch_api_v1',
    'feedcrunch_rssviewer',
    'feedcrunch_rssadmin',
    'feedcrunch_home',
    'oauth',
]

INSTALLED_APPS = THIRD_PARTY_APPS + DJANGO_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'application.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        # 'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
            ],
        },
    },
]

if DEBUG or TESTING:
    TEMPLATES[0]['OPTIONS']['loaders'] = [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}


EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_SES_ACCESS_KEY_ID = assign_env_value('AWS_USER')
AWS_SES_SECRET_ACCESS_KEY = assign_env_value('AWS_SECRET_KEY')
AWS_SES_REGION_NAME = "eu-west-1"
AWS_SES_REGION_ENDPOINT = 'email.eu-west-1.amazonaws.com'
AWS_SES_SENDER = assign_env_value('EMAIL_DEFAULT_SENDER')

WSGI_APPLICATION = 'application.wsgi.application'

FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'application/fixtures/'),
)

ENCRYPTED_FIELDS_KEYDIR = os.path.join(BASE_DIR, 'fieldkeys')
FIELD_ENCRYPTION_KEY= assign_env_value('FIELD_ENCRYPTION_KEY')
# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases


# if True or "test" in sys.argv:
if "test" in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            'CONN_MAX_AGE': 500,
            'TEST':
            {
                'NAME': os.path.join(BASE_DIR, 'db_test.sqlite3'),
            }
        },
    }
else:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(default=assign_env_value('DATABASE_URL'), conn_max_age=500),
    }

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'feedcrunch.FeedUser'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'feedcrunch_cache',
    }
}

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

USER_ESTIMATOR_PATH = "estimators/"
USER_PHOTO_PATH     = "images/user_photos/"
INTEREST_PHOTO_PATH = "images/interest_photos/"

RSS_SUBS_LOOKUP_PERIOD = 3 # (days) Every people visiting the RSS/ATOM feeds over the N last days are count as a subscriber

# MAXIMUM RSS retry
MAX_RSS_RETRIES = 5

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'Europe/Paris'
USE_I18N      = True
USE_L10N      = True
USE_TZ        = True

if not DEBUG and not TESTING:
    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_SECONDS = 3600

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'DENY'

    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

    SECURE_SSL_REDIRECT = True
    SECURE_REDIRECT_EXEMPT = (
        r'^healthcheck\/?$',
        r'^robots\.txt$',
    )

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Celery Configuration
if assign_env_value('USE_RABBITMQ'):
    CELERY_BROKER_URL = assign_env_value('RABBITMQ_URL')
else:
    CELERY_BROKER_URL = assign_env_value('REDIS_URL')

CELERY_BROKER_USE_SSL   = True
CELERY_BROKER_HEARTBEAT = 0

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TIMEZONE       = TIME_ZONE
CELERY_ENABLE_UTC     = False

CELERY_CONCURRENCY       = 3
#CELERY_RESULT_BACKEND   = 'django-db'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_TASK_SERIALIZER            = 'json'
CELERY_TASK_ACKS_LATE             = True # Acknoledge pool when task is over
CELERY_TASK_REJECT_ON_WORKER_LOST = True
CELERY_TASK_RESULT_EXPIRES        = 3*24*60*60 # 3 Days

# Celery Monitor Settings
CELERY_MONITORS_EXPIRE_SUCCESS    = timedelta(hours=1)
CELERY_MONITORS_EXPIRE_ERROR      = timedelta(days=3)
CELERY_MONITORS_EXPIRE_PENDING    = timedelta(days=5)

CELERY_EVENT_QUEUE_EXPIRES = 60
CELERY_EVENT_QUEUE_TTL     = 5

CELERY_TASK_TIME_LIMIT      = 90
CELERY_TASK_SOFT_TIME_LIMIT = 60

if DEBUG or TESTING:
    CELERY_TASK_ALWAYS_EAGER = True
else:
    CELERY_TASK_ALWAYS_EAGER = False

CELERY_TASK_QUEUES = [
    Queue(
        'celery',
        Exchange('celery'),
        routing_key = 'celery',
        queue_arguments = {
            'x-message-ttl': 60 * 1000 # 60 000 ms = 60 secs.
        }
    )
]

CELERYBEAT_SCHEDULER         = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERYBEAT_MAX_LOOP_INTERVAL = 10
CELERYBEAT_SYNC_EVERY        = 1

CELERYBEAT_SCHEDULE = {
    'refresh_all_rss_subscribers_count': {
        'task': 'feedcrunch.tasks.refresh_all_rss_subscribers_count',
        'schedule': crontab(hour=0, minute=5), # Everyday at midnight + 5 mins
        'options': {'expires': 20 * 60} # 20 minutes
    },
    'clean_unnecessary_rss_visits': {
        'task': 'feedcrunch.tasks.clean_unnecessary_rss_visits',
        'schedule': crontab(hour=0, minute=20), # Everyday at midnight + 20 mins
        'options': {'expires': 20 * 60} # 20 minutes
    },
    'celery.backend_cleanup': {
        'task': 'celery.backend_cleanup',
        'schedule': crontab(minute='30'), # Every hours when minutes = 30 mins
        'options': {'expires': 50 * 60} # 50 minutes
    },
    'refresh_all_rss_feeds': {
        'task': 'feedcrunch.tasks.refresh_all_rss_feeds',
        'schedule': crontab(minute='40'), # Every hours when minutes = 40 mins
        'options': {'expires': 30 * 60} # 30 minutes
    },
}

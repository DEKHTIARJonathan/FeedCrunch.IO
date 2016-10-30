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

import os, sys, dj_database_url, getenv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# ================== We append to the path the function folder containing generic functions

functions_dir = os.path.join(BASE_DIR, 'functions')
sys.path.insert(0, functions_dir)

#################################################################################

STATICFILES_LOCATION = 'static'
STATIC_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'staticfiles')

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

if DEBUG:

	# Simplified static file serving.
	# https://warehouse.python.org/project/whitenoise/
	STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
	STATIC_URL = "/%s/" % STATICFILES_LOCATION

	DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
	MEDIA_URL = "/%s/" % MEDIAFILES_LOCATION

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

INSTALLED_APPS = [
	#'grappelli',
	'material',
	#'material.frontend',
	'material.admin',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'storages',
	'feedcrunch',
	'feedcrunch_api_v1',
	'feedcrunch_rssviewer',
	'feedcrunch_rssadmin',
	'feedcrunch_rssadmin_dev',
	'feedcrunch_home',
	'twitter',
	'rest_framework',
]

#TEST_RUNNER = 'junorunner.testrunner.TestSuiteRunner'

MIDDLEWARE_CLASSES = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'django.contrib.staticfiles.storage.StaticFilesStorage',
]

ROOT_URLCONF = 'application.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [],
		'APP_DIRS': True,
		'OPTIONS': {
			'debug': DEBUG,
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

WSGI_APPLICATION = 'application.wsgi.application'

FIXTURE_DIRS = (
	os.path.join(BASE_DIR, 'application/fixtures/'),
)

ENCRYPTED_FIELDS_KEYDIR = os.path.join(BASE_DIR, 'fieldkeys')

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

if "test" in sys.argv:
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.sqlite3',
			'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
			'CONN_MAX_AGE': 500,
			'TEST' :
			{
				'NAME': os.path.join(BASE_DIR, 'db_test.sqlite3'),
			}
		},
	}
else:
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

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
	os.path.join(PROJECT_ROOT, 'static'),
)

USER_PHOTO_PATH = "images/user_photos/"

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

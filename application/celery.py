#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

import os, dotenv

from celery import Celery
from celery.schedules import crontab

import django

platforms = ["TRAVIS", "HEROKU", "BLUEMIX"]

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')

def load_env():
    "Get the path to the .env file and load it."
    project_dir = os.path.dirname(os.path.dirname(__file__))
    dotenv.read_dotenv(os.path.join(project_dir, '.env'))

if not any(x in os.environ for x in platforms):
    load_env()

django.setup()

from django.conf import settings
from django.apps import AppConfig


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')

app = Celery('application')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = settings.CELERYBEAT_SCHEDULE

class CeleryConfig(AppConfig):
    name = 'application'
    verbose_name = 'Celery Config'

@app.task(bind=True)
def debug_task(self):
  print('Request: {0!r}'.format(self.request))

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

import os, dotenv

from celery import Celery
from celery.schedules import crontab

from datetime import timedelta

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
# app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.broker_url                 = settings.BROKER_URL
app.conf.broker_use_ssl             = settings.BROKER_USE_SSL
app.conf.accept_content             = settings.CELERY_ACCEPT_CONTENT
app.conf.timezone                   = settings.CELERY_TIMEZONE

# Worker settings
app.conf.worker_concurrency         = settings.CELERY_CONCURRENCY

# Results settings
#app.conf.result_backend            = settings.CELERY_RESULT_BACKEND
app.conf.result_serializer          = settings.CELERY_RESULT_SERIALIZER
app.conf.result_expires             = settings.CELERY_TASK_RESULT_EXPIRES

# Task settings
app.conf.task_serializer            = settings.CELERY_TASK_SERIALIZER
app.conf.task_acks_late             = settings.CELERY_TASK_ACKS_LATE
app.conf.task_reject_on_worker_lost = settings.CELERY_TASK_REJECT_ON_WORKER_LOST
app.conf.task_time_limit            = settings.CELERY_TASK_TIME_LIMIT
app.conf.task_soft_time_limit       = settings.CELERY_TASK_SOFT_TIME_LIMIT
app.conf.task_always_eager          = settings.CELERY_TASK_ALWAYS_EAGER
app.conf.task_queues                = settings.CELERY_TASK_QUEUES

# Event settings
app.conf.event_queue_ttl            = settings.CELERY_EVENT_QUEUE_EXPIRES
app.conf.event_queue_expires        = settings.CELERY_EVENT_QUEUE_TTL

# Celery Beat Settings
app.conf.beat_scheduler             = settings.CELERYBEAT_SCHEDULER
app.conf.beat_schedule              = settings.CELERYBEAT_SCHEDULE
app.conf.beat_sync_every            = settings.CELERYBEAT_SYNC_EVERY
app.conf.beat_max_loop_interval     = settings.CELERYBEAT_MAX_LOOP_INTERVAL

# Celery Monitor Settings
app.conf.monitors_expire_success    = timedelta(hours=1)
app.conf.monitors_expire_error      = timedelta(days=3)
app.conf.monitors_expire_pending    = timedelta(days=5)

class CeleryConfig(AppConfig):
    name = 'application'
    verbose_name = 'Celery Config'

@app.task(bind=True)
def debug_task(self):
  print('Request: {0!r}'.format(self.request))

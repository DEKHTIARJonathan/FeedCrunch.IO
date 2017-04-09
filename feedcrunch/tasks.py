#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils import timezone

from django_q.tasks import schedule
from django_q.models import Schedule

from .task_files.task_record_rss_subscribers import *
from .task_files.publish_on_social_networks import *
from .task_files.task_refresh_rssfeeds import *
from .task_files.task_send_emails import *

from datetime import timedelta

####################################################################################################################
# ============================================ LAUNCH RECURRING JOB  ============================================= #
####################################################################################################################

def launch_recurrent_rss_job():
    execution_time = timezone.now()
    execution_time = execution_time.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)

    schedule('feedcrunch.tasks.refresh_all_rss_feeds', schedule_type=Schedule.HOURLY, next_run=execution_time)
    schedule('feedcrunch.tasks.refresh_all_rss_subscribers_count', schedule_type=Schedule.DAILY, next_run=execution_time)

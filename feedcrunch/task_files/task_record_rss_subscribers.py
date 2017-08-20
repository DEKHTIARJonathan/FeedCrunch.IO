#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from application.celery import app as celery

from feedcrunch.models import FeedUser, RSSSubsStat

from datetime import timedelta

@celery.task(name='feedcrunch.tasks.record_user_subscribers_stats')
def record_user_subscribers_stats(username=None):
    #try:
        if username is None:
            raise Exception("Username have not been provided")

        try:
            usr = FeedUser.objects.get(username=username)
        except ObjectDoesNotExist:
            raise Exception("The given username ('"+username+"') doesn't exist.")

        today           = timezone.now().date()
        yesterday       = today - timedelta(days=1)
        sub_timedelta   = settings.RSS_SUBS_LOOKUP_PERIOD
        last_lookup_day = today - timedelta(days=sub_timedelta)

        if not usr.rel_rss_subscribers_count.filter(date__gte=yesterday).exists(): # Check if a statistic already exists for yesterday

            count = usr.rel_rss_subscribers.filter(date__gte=last_lookup_day).values("ipaddress").annotate(n=models.Count("pk")).count()

            record = RSSSubsStat.objects.create(user=username, count=count)

            if isinstance(record, dict):
                raise Exception(record["error"] + " // Timestamp: " + record["timestamp"].strftime("%d/%m/%y - %H:%M") + " // Timestamp_TZ: " + record["timestamp_tz"].strftime("%d/%m/%y - %H:%M"))

        else:
            raise Exception("Object already exists with date: " + yesterday.strftime("%d/%m/%y") + " & it happened at date : " + timezone.now().strftime("%d/%m/%y - %H:%M"))

    #except Exception as e:
    #    raise Exception("Error: tasks.record_user_subscribers_stats - Error: " + str(e))


@celery.task(name='feedcrunch.tasks.refresh_all_rss_subscribers_count')
def refresh_all_rss_subscribers_count():
    for user in FeedUser.objects.all():
        record_user_subscribers_stats.delay(username=user.username)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.conf import settings
#from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
#from django.template.loader import render_to_string
from django.utils import timezone

from django_q.tasks import schedule
from django_q.models import Schedule

from feedcrunch.models import FeedUser, RSSSubsStat
#from feedcrunch.models import FeedUser, RSSFeed, RSSSubscriber,

from datetime import timedelta


def record_user_subscribers_stats(username=None):
    if username is not None:

        try:
            usr = FeedUser.objects.get(username=username)
        except ObjectDoesNotExist:
            raise Exception("The given username ('"+username+"') doesn't exist.")

        today           = timezone.now().date()
        sub_timedelta   = settings.RSS_SUBS_LOOKUP_PERIOD
        last_lookup_day = today - timedelta(days=sub_timedelta)

        if not usr.rel_rss_subscribers_count.filter(date=timezone.now().date()).exists(): # Check if a statistic already exists for that day

            #count = usr.rel_rss_subscribers.filter(date__range=(last_lookup_day, today)).values("ipaddress").annotate(n=models.Count("pk")).count()__gte
            count = usr.rel_rss_subscribers.filter(date__gte=last_lookup_day).values("ipaddress").annotate(n=models.Count("pk")).count()

            RSSSubsStat.objects.create(user=username, count=count)

    else:
        raise Exception("Error: tasks.record_user_subscribers_stats - username have not been provided.")

def refresh_all_rss_subscribers_count():
    for user in FeedUser.objects.all():
        schedule('feedcrunch.tasks.record_user_subscribers_stats', username=user.username, schedule_type=Schedule.ONCE, next_run=timezone.now() + timedelta(minutes=1))

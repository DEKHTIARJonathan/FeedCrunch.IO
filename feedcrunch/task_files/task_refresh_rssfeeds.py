#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

#from django.db import models
#from django.conf import settings
#from django.core.mail import send_mail
#from django.core.exceptions import ObjectDoesNotExist
#from django.template.loader import render_to_string
from django.utils import timezone

from django_q.tasks import schedule
from django_q.models import Schedule

from feedcrunch.models import FeedUser, RSSFeed

#from feedcrunch.models import FeedUser, RSSFeed, RSSSubscriber, RSSSubsStat

from datetime import timedelta


def check_rss_feed(rss_id):
    RSSFeed.objects.get(id=rss_id).refresh_feed()

def refresh_user_rss_subscribtions(username=None):
    if username is not None:
        FeedUser.objects.get(username=username).refresh_user_subscribtions()
    else:
        raise Exception("Error: tasks.refresh_user_rss_subscribtions - username have not been provided.")

def refresh_all_rss_feeds():
    for feed in RSSFeed.objects.all():
        schedule('feedcrunch.tasks.check_rss_feed', rss_id=feed.id, schedule_type=Schedule.ONCE, next_run=timezone.now() + timedelta(minutes=1))

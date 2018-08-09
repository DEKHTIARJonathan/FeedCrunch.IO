#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from application.celery import app as celery

from feedcrunch.models import FeedUser
from feedcrunch.models import RSSFeed

__all__ = [
    'check_rss_feed',
    'refresh_user_rss_subscriptions',
    'refresh_all_rss_feeds',
]


@celery.task(name='feedcrunch.tasks.check_rss_feed')
def check_rss_feed(rss_id):
    RSSFeed.objects.get(id=rss_id).refresh_feed()


@celery.task(name='feedcrunch.tasks.refresh_user_rss_subscriptions')
def refresh_user_rss_subscriptions(username=None):
    if username is not None:
        FeedUser.objects.get(username=username).refresh_user_subscriptions()
    else:
        raise Exception("Error: tasks.refresh_user_rss_subscriptions - username have not been provided.")


@celery.task(name='feedcrunch.tasks.refresh_all_rss_feeds')
def refresh_all_rss_feeds():
    for feed in RSSFeed.objects.all():
        check_rss_feed.delay(rss_id=feed.id)

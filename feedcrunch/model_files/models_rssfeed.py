#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unicodedata
import feedparser

from django.db import models
from django.conf import settings

from functions.get_domain import get_domain
from functions.clean_html import clean_html
from functions.feed_validation import validate_feed


class RSSFeedManager(models.Manager):
    def create(self, *args, **kwargs):

        if 'title' in kwargs and (isinstance(kwargs['title'], str) or isinstance(kwargs['title'], str)):
            kwargs['title'] = clean_html(kwargs['title'])
        else:
            raise Exception("Title is missing - RSSFeed Manager")

        if 'link' in kwargs and (isinstance(kwargs['link'], str) or isinstance(kwargs['link'], str)):

            if RSSFeed.objects.filter(link=kwargs['link']).exists():
                raise Exception("RSSFeed already exists in the database.")

            elif not validate_feed(kwargs['link']):
                raise Exception("RSS Feed is not valid")

        else:
            raise Exception("Link is missing - RSSFeed Manager")

        return super(RSSFeedManager, self).create(*args, **kwargs)


class RSSFeed(models.Model):
    objects = RSSFeedManager()

    id           = models.AutoField(primary_key=True)
    title        = models.CharField(max_length=255)
    link         = models.URLField(max_length=2000)
    added_date   = models.DateTimeField(auto_now_add=True)
    active       = models.BooleanField(default=True)
    bad_attempts = models.SmallIntegerField(default=0)
    error        = models.CharField(max_length=255, default='', blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.id is not None:
            self.title = clean_html(self.title)

            old_version = RSSFeed.objects.get(id=self.id)
            if (self.link != old_version.link) and (not validate_feed(self.link)):
                raise Exception("RSS Feed is not valid")

        super(RSSFeed, self).save(*args, **kwargs) # Call the "real" save() method.

    def get_date(self):
        return self.added_date.strftime("%Y/%m/%d %H:%M")

    def get_shortdate(self):
        return self.added_date.strftime("%Y/%m/%d")

    def get_domain(self):
        return get_domain(self.link)

    def count_articles(self):
        return self.rel_rss_feed_articles.count()

    def count_subscribers(self):
        return self.rel_sub_feed_assoc.count()

    def get_subscribers(self):
        RSSFeed_Sub_queryset = self.rel_sub_feed_assoc.all()

        rslt = []
        for sub in RSSFeed_Sub_queryset:
            rslt.append(sub.user)

        return rslt

    def _set_inactive_feed(error=""):
        self.active = False
        self.error = error
        self.save()

    def _trigger_bad_attempt(self):
        self.bad_attempts += 1

        if self.bad_attempts >= settings.MAX_RSS_RETRIES:
            _set_inactive_feed(error="Too many bad attempts to download the feed")
        else:
            self.save()

    def _reset_bad_attempts(self):
        self.bad_attempts = 0
        self.error = ""
        self.active = True
        self.save()

    def refresh_feed(self):
        from .models_rss_assocs import RSSArticle_Assoc

        try:
            if (self.active and self.count_subscribers() > 0):

                from .models_rssarticle import RSSArticle

                while True:
                    feed_content = feedparser.parse(self.link)

                    if feed_content.bozo != 0:
                        self._set_inactive_feed(error="The feed can not be validated.")
                        return True

                    elif feed_content.status in [301, 302]:
                        try:
                            self.link = feed_content['feed']['title_detail']['base']
                            self.save()

                        except Exception:

                            try:
                                old_link = self.link

                                for item in feed_content['feed']["links"]:

                                    if "rss" in item['type'] or "atom" in item['type']:
                                        self.link = item["href"]
                                        self.save()

                                if self.link == old_link:
                                    self._set_inactive_feed(error="Impossible to find any new link in the list of links")
                                    return True

                            except Exception as e:
                                self._set_inactive_feed(error="No existing link found, please check the feed")
                                return True

                    elif 400 <= feed_content.status <= 599:
                        self._set_inactive_feed(error="The request ended with the error code: " + str(feed_content.status))
                        return True

                    else:
                        break

                if feed_content.status == 200:

                    self._reset_bad_attempts()

                    for entry in feed_content['entries']:

                        if 'title' in entry:
                            title = unicodedata.normalize('NFC', entry["title"])
                        else:
                            continue

                        if 'link' in entry:
                            link = unicodedata.normalize('NFC', entry["link"])
                        elif 'links' in entry:
                            link = unicodedata.normalize('NFC', entry["links"][0]["href"])
                        else:
                            continue

                        try:
                            tmp_article = RSSArticle.objects.create(rssfeed=self, title=title, link=link)
                            subscriptions = self.rel_sub_feed_assoc.all()

                            for subscription in subscriptions:
                                try:
                                    RSSArticle_Assoc.objects.create(subscription=subscription, user=subscription.user, article=tmp_article)
                                except Exception as e:
                                    raise Exception("Exception occured while creating RSSArticle_Assoc object: " + str(e))

                        except Exception as e:
                            raise Exception("Exception occured : " + str(e))

                else:
                    self._trigger_bad_attempt()
                    raise Exception("Feed ID = " + str(self.id) + " can't be downloaded to server. Status = " + str(feed_content.status))

        except Exception as e:
            return "An error occured in the process: " + str(e)

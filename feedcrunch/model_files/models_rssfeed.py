#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.conf import settings

import datetime, string, re, unicodedata, feedparser, HTMLParser

from .models_user import FeedUser

from get_domain import get_domain
from clean_html import clean_html

from feed_validation import validate_feed

class RSSFeedManager(models.Manager):
	def create(self, *args, **kwargs):

		if 'title' in kwargs and (isinstance(kwargs['title'], str) or isinstance(kwargs['title'], unicode)):
			kwargs['title'] = clean_html(kwargs['title'])
		else:
			raise Exception("Title is missing - RSSFeed Manager")

		if 'link' in kwargs and (isinstance(kwargs['link'], str) or isinstance(kwargs['link'], unicode)):

			if not validate_feed(kwargs['link']):
				raise Exception("RSS Feed is not valid")

			elif RSSFeed.objects.filter(link=kwargs['link'], user=kwargs['user']).exists():
				raise Exception("User already subscribed to this feed.")

		else:
			raise Exception("Link is missing - RSSFeed Manager")

		return super(RSSFeedManager, self).create(*args, **kwargs)

class RSSFeed(models.Model):
	objects = RSSFeedManager()

	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=255)
	link = models.URLField(max_length=2000)
	added_date = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)
	bad_attempts = models.SmallIntegerField(default=0)

	def __unicode__(self):
		return self.title

	def save(self, *args, **kwargs):
		self.title = clean_html(self.title)

		if not validate_feed(self.link):
			raise Exception("RSS Feed is not valid")

		if RSSFeed.objects.filter(user=self.user, link=self.link).exclude(id=self.id).exists():
			raise Exception("User already subscribed to this feed.")

		super(RSSFeed, self).save(*args, **kwargs) # Call the "real" save() method.

	def get_date(self):
		return self.added_date.strftime("%Y/%m/%d %H:%M")

	def get_shortdate(self):
		return self.added_date.strftime("%Y/%m/%d")

	def get_domain(self):
		return get_domain(self.link)

	def count_articles(self):
		return self.rel_rss_feed_articles.count()

	def _trigger_bad_attempt(self):
		self.bad_attempts += 1
		if self.bad_attempts >= settings.MAX_RSS_RETRIES:
			self.active = False
		self.save()

	def _reset_bad_attempts(self):
		if (self.bad_attempts != 0 or self.active == False):
			self.bad_attempts = 0
			self.active = True
			self.save()

	def refresh_feed(self):
		try:
			if (self.active):
				from .models_rssarticle import RSSArticle

				feed_content = feedparser.parse(self.link)

				if feed_content.status == 200:

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

						if not RSSArticle.objects.filter(rssfeed=self, link=link).exists():
							RSSArticle.objects.create(rssfeed=self, title=title, link=link)
							subscribers = self.rel_sub_feed_assoc.all()

					self._reset_bad_attempts()

				else:
					raise Exception("Feed ID = " + str(self.id) + " can't be downloaded to server. Status = " + str(feed_content.status))

			else:
				raise Exception("Feed ID = " + str(self.id) + " is not active.")

		except Exception, e:
			print "An error occured in the process: " + str(e)
			self._trigger_bad_attempt()

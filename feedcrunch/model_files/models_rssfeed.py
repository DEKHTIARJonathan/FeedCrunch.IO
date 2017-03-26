#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.conf import settings

import datetime, string, re, unicodedata, feedparser

from get_domain import get_domain
from clean_html import clean_html

from feed_validation import validate_feed

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

	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=255)
	link = models.URLField(max_length=2000)
	added_date = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)
	bad_attempts = models.SmallIntegerField(default=0)

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
		from .models_rss_assocs import RSSArticle_Assoc

		try:
    		if (self.active and self.count_subscribers() > 0):

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

    					try:
    						tmp_article = RSSArticle.objects.create(rssfeed=self, title=title, link=link)
    						subscribtions = self.rel_sub_feed_assoc.all()

    						for subscribtion in subscribtions:
    							try:
    								RSSArticle_Assoc.objects.create(subscribtion=subscribtion, user=subscribtion.user, article=tmp_article)
    							except Exception as e:
    								print (str(e))
    								pass
    					except:
    						pass

    				self._reset_bad_attempts()

    			else:
    				raise Exception("Feed ID = " + str(self.id) + " can't be downloaded to server. Status = " + str(feed_content.status))

		except Exception as e:
			print ("An error occured in the process: " + str(e))
			#self._trigger_bad_attempt()

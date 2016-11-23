#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

import datetime, string, re, uuid

from .models_rssfeed import RSSFeed

from get_domain import get_domain
from clean_html import clean_html

class RSSArticleManager(models.Manager):
	def create(self, *args, **kwargs):

		if 'title' in kwargs and (isinstance(kwargs['title'], str) or isinstance(kwargs['title'], unicode)):
			kwargs['title'] = clean_html(kwargs['title'])
		else:
			raise Exception("Title is missing - RSSArticle Manager")

		if 'link' in kwargs and (isinstance(kwargs['link'], str) or isinstance(kwargs['link'], unicode)):
			if RSSArticle.objects.filter(rssfeed=kwargs['rssfeed'], link=kwargs['link']).exists():
				raise Exception("RSS Article already exists in database - RSSArticle Manager")

		else:
			raise Exception("Link is missing - RSSFeed Manager")

		return super(RSSArticleManager, self).create(*args, **kwargs)

class RSSArticle(models.Model):
	objects = RSSArticleManager()

	id = models.AutoField(primary_key=True)
	rssfeed = models.ForeignKey(RSSFeed, related_name='rel_rss_feed_articles', on_delete=models.SET_NULL, null=True)
	title = models.CharField(max_length=255)
	link = models.URLField(max_length=2000)
	description = models.TextField(default='', blank=True, null=True)
	guid = models.UUIDField(default=uuid.uuid4, editable=True, blank=True, null=True)
	creator = models.CharField(max_length=255, default='', blank=True, null=True)
	content = models.TextField(default='', blank=True, null=True)
	media = models.CharField(max_length=255, default='', blank=True, null=True)
	pub_date = models.CharField(max_length=255, default='', blank=True, null=True)
	added_date = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.title

	def save(self, *args, **kwargs):
		if self.id is not None:
			self.title = clean_html(self.title)
		super(RSSArticle, self).save(*args, **kwargs) # Call the "real" save() method.

	def get_date(self):
		return self.added_date.strftime("%Y/%m/%d %H:%M")

	def get_shortdate(self):
		return self.added_date.strftime("%Y/%m/%d")

	def get_domain(self):
		return get_domain(self.link)

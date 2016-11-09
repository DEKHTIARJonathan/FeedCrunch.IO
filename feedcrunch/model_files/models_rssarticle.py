#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

import datetime, string, re, uuid

from .models_user import *
from .models_rssfeed import *

class RSSArticle(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(FeedUser, related_name='rel_rss_user_articles')
	rssfeed = models.ForeignKey(RSSFeed, related_name='rel_rss_feed_articles')
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
		return str(self.title)

	def get_date(self):
		return self.added_date.strftime("%Y/%m/%d %H:%M")

	def get_shortdate(self):
		return self.added_date.strftime("%Y/%m/%d")

	def get_domain(self):
		starts = [match.start() for match in re.finditer(re.escape("/"), self.link)]
		if len(starts) > 2:
			return self.link[starts[1]+1:starts[2]]
		elif len(starts) == 2:
			return self.link[starts[1]+1:]
		else:
			return str("error")

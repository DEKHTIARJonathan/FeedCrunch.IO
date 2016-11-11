#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

import datetime, string, re, unicodedata

from .models_user import *

class RSSFeed(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(FeedUser, related_name='rel_feeds')
	title = models.CharField(max_length=255)
	link = models.URLField(max_length=2000)
	added_date = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.title

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

	def refresh_feed(self):
		from .models_rssarticle import RSSArticle

		feed_content = feedparser.parse(self.link)

		if (feed_content.bozo == 0):

			for entry in feed_content['entries']:

				if 'title' in entry:
					title = unicodedata.normalize('NFKD', entry["title"]).encode('ascii','ignore')
				else:
					continue

				if 'link' in entry:
					link = entry["link"]
				elif 'links' in entry:
					link = entry["links"][0]["href"]
				else:
					continue

				if not RSSArticle.objects.filter(user=self.user, rssfeed=self, title=title, link=link).exists():
					article_tmp = RSSArticle.objects.create(user=self.user, rssfeed=self, title=title, link=link)
					article_tmp.save()

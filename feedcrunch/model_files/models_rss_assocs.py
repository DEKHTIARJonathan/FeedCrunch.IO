#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

import datetime, string, re, uuid

from .models_user import FeedUser
from .models_rssfeed import RSSFeed
from .models_rssarticle import RSSArticle


class RSSFeed_Sub(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(FeedUser, related_name='rel_sub_user')
	feed = models.ForeignKey(RSSFeed, related_name='rel_sub_feed_assoc')

	title = models.CharField(max_length=255)
	added_date = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.title

	class Meta:
		unique_together = ("user", "feed")


class RSSArticle_Assoc(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(FeedUser, related_name='rel_sub_article')
	article = models.ForeignKey(RSSArticle, related_name='rel_sub_article_assoc')

	open_count = models.SmallIntegerField(default=0)
	marked_read = models.BooleanField(default=False)
	reposted = models.BooleanField(default=False)
	recommendation_score = models.FloatField(default=0)

	class Meta:
		unique_together = ("user", "article")

	def __unicode__(self):
		return self.get_title()

	def get_title(self):
		return self.article.title

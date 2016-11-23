#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

import datetime, string, re, uuid

from .models_user import FeedUser
from .models_rssfeed import RSSFeed
from .models_rssarticle import RSSArticle

from clean_html import clean_html

class RSSFeed_SubManager(models.Manager):
	def create(self, *args, **kwargs):

		if 'title' in kwargs and (isinstance(kwargs['title'], str) or isinstance(kwargs['title'], unicode)):
			kwargs['title'] = clean_html(kwargs['title'])
		else:
			raise Exception("Title is missing - RSSFeed_Sub Manager")

		if RSSFeed_Sub.objects.filter(user=kwargs['user'], feed=kwargs['feed']).exists():
			raise Exception("User ("+kwargs['user'].username+") is already subscribed to the RSSFeed (id = "+str(kwargs['feed'].id)+")")

		return super(RSSFeed_SubManager, self).create(*args, **kwargs)

class RSSFeed_Sub(models.Model):
	objects = RSSFeed_SubManager()

	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(FeedUser, related_name='rel_sub_user')
	feed = models.ForeignKey(RSSFeed, related_name='rel_sub_feed_assoc')

	title = models.CharField(max_length=255, blank=False, null=False)
	added_date = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.title

	class Meta:
		unique_together = ("user", "feed")

	def save(self, *args, **kwargs):
		if self.id is not None:
			self.title = clean_html(self.title)
		super(RSSFeed_Sub, self).save(*args, **kwargs) # Call the "real" save() method.


###################################################################################################################################

class RSSArticle_AssocManager(models.Manager):
	def create(self, *args, **kwargs):

		if RSSArticle_Assoc.objects.filter(user=kwargs['user'], article=kwargs['article']).exists():
			raise Exception("User ("+kwargs['user'].username+") is already associated with RSSArticle (id = "+str(kwargs['article'].id)+")")

		return super(RSSArticle_AssocManager, self).create(*args, **kwargs)

class RSSArticle_Assoc(models.Model):
	objects = RSSArticle_AssocManager()

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

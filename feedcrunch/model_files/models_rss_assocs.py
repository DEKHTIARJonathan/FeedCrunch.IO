#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

import datetime, string, re, uuid

from .models_user import FeedUser
from .models_rssfeed import RSSFeed
from .models_rssarticle import RSSArticle

from clean_html import clean_html

def shorten_string(string, max_size):
	if max_size < 7:
		max_size = 7
	if (len(string) > max_size):
		return string[:max_size-6] + " [...]"
	else:
		return string

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
	user = models.ForeignKey(FeedUser, related_name='rel_sub_feed', on_delete=models.CASCADE)
	feed = models.ForeignKey(RSSFeed, related_name='rel_sub_feed_assoc', on_delete=models.CASCADE)

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

	def count_articles(self):
		return self.rel_sub_feedsub_article.count()

	def link(self):
		return self.feed.link

	def short_link(self):
		return shorten_string(self.feed.link, 35)

	def get_domain(self):
		return self.feed.get_domain()

	def short_domain(self):
		return shorten_string(self.get_domain(), 25)

	def short_title(self):
		return shorten_string(self.title, 75)


###################################################################################################################################

class RSSArticle_AssocManager(models.Manager):
	def create(self, *args, **kwargs):

		if RSSArticle_Assoc.objects.filter(user=kwargs['user'], article=kwargs['article']).exists():
			raise Exception("User ("+kwargs['user'].username+") is already associated with RSSArticle (id = "+str(kwargs['article'].id)+")")

		return super(RSSArticle_AssocManager, self).create(*args, **kwargs)

class RSSArticle_Assoc(models.Model):
	objects = RSSArticle_AssocManager()

	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(FeedUser, related_name='rel_sub_article', on_delete=models.CASCADE)
	article = models.ForeignKey(RSSArticle, related_name='rel_sub_article_assoc', on_delete=models.CASCADE)
	subscribtion = models.ForeignKey(RSSFeed_Sub, related_name='rel_sub_feedsub_article', on_delete=models.SET_NULL, null=True)

	open_count = models.SmallIntegerField(default=0)
	marked_read = models.BooleanField(default=False)
	reposted = models.BooleanField(default=False)
	recommendation_score = models.FloatField(default=0)

	class Meta:
		unique_together = ("user", "article")

	def __unicode__(self):
		return self.title()

	def title(self):
		return self.article.title

	def short_title(self):
		return shorten_string(self.article.title, 75)

	def link(self):
		return self.article.link

	def get_domain(self):
		return self.article.get_domain()

	def short_domain(self):
		return shorten_string(self.article.get_domain(), 35)

	def rssfeed(self):
		if self.subscribtion is not None: # Subscribed to the RSSFeed
			return self.subscribtion.title
		else: # Not subscribed anymore to the RSSFeed
			return self.article.rssfeed.title

	def short_rssfeed(self):
		return shorten_string(self.rssfeed(), 35)

	def get_shortdate(self):
		return self.article.get_shortdate()

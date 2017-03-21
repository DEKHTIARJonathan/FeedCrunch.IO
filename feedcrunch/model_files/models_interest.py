#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.conf import settings

from .models_rssfeed import RSSFeed

import random, urllib, string, uuid

############################## Interest MODEL ###################################

def id_generator(size=20, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def get_photo_path(instance, filename):
	ext = filename.split('.')[-1]

	while True:
		filename = "%s.%s" % (id_generator(), ext)

		photo_url = "%s%s" % (settings.MEDIA_URL, filename)

		if settings.DEBUG or urllib.urlopen(photo_url).getcode() != 200:
			break

	return settings.INTEREST_PHOTO_PATH + filename

class Interest(models.Model):
	name = models.CharField(max_length=255, primary_key=True)
	rssfeeds = models.ManyToManyField(RSSFeed, blank=True, related_name='rel_interests')
	picture = models.ImageField(upload_to=get_photo_path, default=settings.INTEREST_PHOTO_PATH+'dummy_stock.jpg', blank=True, null=True)
	guid = models.UUIDField(default=uuid.uuid4, editable=False, blank=False, null=False, unique=True)

	def __str__(self):
		return self.name

	def get_photo_path(self):
		if settings.DEBUG:
			return self.picture.url
		else:
			photo_url = "%s%s" % (settings.MEDIA_URL, self.picture)
			return photo_url

	def get_rssfeed_count(self):
		return self.rssfeeds.count()

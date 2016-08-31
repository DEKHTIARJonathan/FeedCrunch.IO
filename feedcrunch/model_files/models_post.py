#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User, UserManager

import re, uuid, datetime

from .models_geo import *
from .models_user import *
from .models_tag import *

############################## ARTICLE MODEL ###################################

class Post(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(FeedUser)
	title = models.CharField(max_length=255)
	link = models.URLField(max_length=2000)
	when = models.DateTimeField(auto_now_add=True)
	clicks = models.IntegerField()
	activeLink = models.BooleanField()
	tags = models.ManyToManyField(Tag, blank=True, related_name='rel_posts')

	def __unicode__(self):
		return str(self.id)

	def get_date(self):
		return self.when.strftime("%Y/%m/%d %H:%M")

	def get_domain(self):
		starts = [match.start() for match in re.finditer(re.escape("/"), self.link)]
		if len(starts) > 2:
			return self.link[starts[1]+1:starts[2]]
		elif len(starts) == 2:
			return self.link[starts[1]+1:]
		else:
			return str("error")

	def get_tags(self):
		output = ""
		for tag in self.tags.all():
			output += str(tag) + " "
		return str(output)[:-1] # We remove the last space before returning the value

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

import datetime, string, re

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

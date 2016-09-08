#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

############################## TAG MODEL ###################################

class Tag(models.Model):
	name = models.CharField(max_length=30, primary_key=True)

	def __unicode__(self):
		return self.name

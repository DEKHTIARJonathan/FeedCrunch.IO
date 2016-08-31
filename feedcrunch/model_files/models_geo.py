#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User, UserManager

############################# Localisation #####################################

class Continent(models.Model):
	name = models.CharField(primary_key=True, max_length=60)
	code = models.CharField(max_length=2)

	def __unicode__(self):
		return self.name

class Country(models.Model):
	name = models.CharField(primary_key=True, max_length=60)
	code = models.CharField(max_length=2)
	continent = models.ForeignKey(Continent)

	def __unicode__(self):
		return self.name

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

from encrypted_model_fields .fields import EncryptedCharField

############################## Option MODEL ###################################

class Option(models.Model):
	parameter = models.CharField(max_length=255, primary_key=True)
	value = EncryptedCharField(max_length=255, default='')

	def __unicode__(self):
		return self.parameter

	def get_bool_value(self):
		return self.value.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']

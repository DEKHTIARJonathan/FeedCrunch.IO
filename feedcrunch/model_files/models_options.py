# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from encrypted_fields import EncryptedCharField

############################## ARTICLE MODEL ###################################

class Options(models.Model):
	parameter = models.CharField(max_length=255, primary_key=True)
	value = EncryptedCharField(max_length=255, default='')

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

############################# Localisation #####################################

class Continent(models.Model):
    name = models.CharField(primary_key=True, max_length=60)
    code = models.CharField(max_length=2)

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(primary_key=True, max_length=60)
    code = models.CharField(max_length=2)
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

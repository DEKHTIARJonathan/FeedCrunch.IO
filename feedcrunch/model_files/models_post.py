#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User, UserManager

import re, uuid, datetime, random, string

from .models_geo import *
from .models_user import *
from .models_tag import *

from get_domain import get_domain

def create_key(size=8):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(size))

############################## Post MODEL ###################################

class Post(models.Model):
    id         = models.AutoField(primary_key=True)
    user       = models.ForeignKey(FeedUser, related_name='rel_posts', on_delete=models.CASCADE)
    title      = models.CharField(max_length=255)
    link       = models.URLField(max_length=2000)
    when       = models.DateTimeField(auto_now_add=True)
    key        = models.CharField(max_length=8, default=create_key, blank=False, null=False)
    clicks     = models.IntegerField()
    activeLink = models.BooleanField()
    tags       = models.ManyToManyField(Tag, blank=True, related_name='rel_posts')

    def __str__(self):
        return str(self.id)

    def get_date(self):
        return self.when.strftime("%Y/%m/%d %H:%M")

    def get_shortdate(self):
        return self.when.strftime("%Y/%m/%d")

    def get_domain(self):
        return get_domain(self.link)

    def get_tags(self):
        output = ""
        for tag in self.tags.all():
            output += str(tag) + ","
        return str(output)[:-1] # We remove the last space before returning the value

    def get_tags_count(self):
        return self.tags.count()

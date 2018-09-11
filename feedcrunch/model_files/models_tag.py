#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models


############################## TAG MODEL ###################################

class Tag(models.Model):
    name = models.CharField(max_length=30, primary_key=True, editable=False, blank=False, null=False)

    def __str__(self):
        return self.name

    def get_post_count(self):
        return self.rel_posts.count()

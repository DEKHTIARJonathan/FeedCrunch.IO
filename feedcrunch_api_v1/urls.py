#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf import settings
from django.conf.urls import include, url
import django.contrib.auth.views

#from .admin import admin_site
from .views import *

urlpatterns = [
	url(r'^public/get/validate/username/(?P<username>\w+)/$', validate_username, name='validate_username'),
	url(r'^public/get/validate/username/$', validate_username, name='validate_username'),
]

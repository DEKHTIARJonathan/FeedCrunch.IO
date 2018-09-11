#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import url
from oauth.views import *

urlpatterns = [
    url(r'^twitter/get_callback/$', twitter_callback, name='twitter_callback'),
    url(r'^facebook/get_callback/$', facebook_callback, name='facebook_callback'),
    url(r'^linkedin/get_callback/$', linkedin_callback, name='linkedin_callback'),
    url(r'^slack/get_callback/$', slack_callback, name='slack_callback'),
]

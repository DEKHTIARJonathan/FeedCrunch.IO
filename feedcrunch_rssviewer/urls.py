#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import url

from feedcrunch_rssviewer.views import *


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^search/$', search, name='search'),
    url(r'^rss/$', rss_feed, name='rss_feed'),
    url(r'^atom/$', atom_feed, name='atom_feed'),
    url(r'^dataset/$', dataset, name='dataset'),
    url(r'^redirect/(?P<postID>\w+)/$', redirect, name='redirect_page'),
]

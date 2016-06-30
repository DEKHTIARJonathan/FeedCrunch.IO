# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.conf import settings

#from .admin import admin_site
from .views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^search/', search, name='search'),
    url(r'^rss/', rss_feed, name='rss_feed'),
    url(r'^atom/', atom_feed, name='atom_feed'),
    url(r'^redirect/(?P<postID>\w+)/$', redirect, name='redirect_page'),
]

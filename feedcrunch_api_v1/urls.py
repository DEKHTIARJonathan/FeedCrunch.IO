#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf import settings
from django.conf.urls import include, url
import django.contrib.auth.views

#from .admin import admin_site
from .views import *

urlpatterns = [
	#Public API Routes
	url(r'^public/get/validate/username/(?P<username>\w+)/$', Username_Validation.as_view(), name='validate_username'),
	url(r'^public/get/validate/username/$', Username_Validation.as_view(), name='validate_username'),

	#Authentication Required API Routes
	url(r'^authenticated/get/user/publications_stats/$', User_Stats_Publications.as_view(), name='publications_stats'),
	url(r'^authenticated/get/user/subscribers_stats/$', User_Stats_Subscribers.as_view(), name='subscribers_stats'),
	url(r'^authenticated/modify/user/social-networks/$', Modify_Social_Networks.as_view(), name='modify_social_networks'),
	url(r'^authenticated/modify/user/personal-info/$', Modify_Personal_info.as_view(), name='Modify_Personal_info'),

	url(r'^authenticated/get/tags/$', Tags.as_view(), name='tags_as_json'),
	url(r'^authenticated/post/article/$', Article.as_view(), name='post_article'),
	url(r'^authenticated/modify/article/(?P<postID>\d+)/$', Article.as_view(), name='modify_article'),
	url(r'^authenticated/delete/article/(?P<postID>\d+)/$', Article.as_view(), name='delete_article'),


	#Private API Routes - API KEY REQUIRED
	url(r'^private/get/article/(?P<postID>\d+)/$', Article.as_view(), name='get_article'),
]

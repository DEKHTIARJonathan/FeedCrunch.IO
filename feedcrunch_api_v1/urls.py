#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf import settings
from django.conf.urls import include, url
import django.contrib.auth.views

#from .admin import admin_site
from .views import *

urlpatterns = [

	# ====================== Public API Routes ====================== #

	url(r'^public/post/validate/username/$', Username_Validation.as_view(), name='validate_username'),
	url(r'^public/post/validate/rssfeed/$', rssfeed_Validation.as_view(), name='validate_username'),

	# ====================== Authentication Required API Routes ====================== #

	# User Routes
	url(r'^authenticated/get/user/publications_stats/$', User_Stats_Publications.as_view(), name='publications_stats'),
	url(r'^authenticated/get/user/subscribers_stats/$', User_Stats_Subscribers.as_view(), name='subscribers_stats'),
	url(r'^authenticated/modify/user/social-networks/$', Modify_Social_Networks.as_view(), name='modify_social_networks'),
	url(r'^authenticated/modify/user/personal-info/$', Modify_Personal_info.as_view(), name='Modify_Personal_info'),
	url(r'^authenticated/modify/user/password/$', Modify_Password.as_view(), name='Modify_Password'),

	# Tag Routes
	url(r'^authenticated/get/tags/$', Tags.as_view(), name='tags_as_json'),

	# RSSArticle Routes
	url(r'^authenticated/mark_as_read/rssarticle/(?P<RSSArticle_AssocID>\d+)/$', RSSArticle_Assoc_View.as_view(), name='Mark_As_Read_RSSArticle_Assoc'),
	url(r'^authenticated/mark_list_as_read/rssarticle/$', RSSArticle_Assoc_View.as_view(), name='Mark_List_As_Read_RSSArticle_Assoc'),


	# RSSFeed Subscribtions Routes
	url(r'^authenticated/post/rssfeed_subscribtion/$', RSSFeed_View.as_view(), name='create_RSSFeed'),
	url(r'^authenticated/delete/rssfeed_subscribtion/(?P<feedID>\d+)/$', RSSFeed_View.as_view(), name='delete_RSSFeed'),
	url(r'^authenticated/modify/rssfeed_subscribtion/(?P<feedID>\d+)/$', RSSFeed_View.as_view(), name='modify_RSSFeed'),

	# Article Routes
	url(r'^authenticated/post/article/$', Article.as_view(), name='post_article'),
	url(r'^authenticated/modify/article/(?P<postID>\d+)/$', Article.as_view(), name='modify_article'),
	url(r'^authenticated/delete/article/(?P<postID>\d+)/$', Article.as_view(), name='delete_article'),

	# ====================== Private API Routes - API KEY REQUIRED ====================== #

	# Article Routes
	url(r'^private/get/article/(?P<postID>\d+)/$', Article.as_view(), name='get_article'),
]

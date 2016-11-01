#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import include, url
from django.conf import settings

#from .admin import admin_site
from .views import *

urlpatterns = [
	url(r'^$', dummy, name='index'),
	url(r'^edit_profile/social/$', dummy, name='update_social_links'),
	url(r'^edit_profile/password/$', update_password, name='update_password'),
	url(r'^edit_profile/info/$', dummy, name='update_info'),
	url(r'^edit_profile/photo/$', update_photo, name='update_info'),
	url(r'^add/ajax/$', dummy, name='add_ajax'),
	url(r'^add/$', dummy, name='add'),
	url(r'^modify/(?P<postID>\d+)/ajax/$', dummy, name='modify_ajax'),
	url(r'^modify/(?P<postID>\d+)/$', dummy, name='modify_listing'),
	url(r'^modify/$', dummy, name='modify_listing'),
	url(r'^delete/ajax/$', dummy, name='delete_ajax'),
	url(r'^delete/$', dummy, name='delete_listing'),
	url(r'^tags/json/$', dummy, name='add_ajax'),
]

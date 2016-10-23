#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import include, url
from django.conf import settings

#from .admin import admin_site
from .views import *

urlpatterns = [
	url(r'^$', index, name='dashboard'),
	url(r'^account/info/$', personal_info_form, name='personal_info_form'),
	url(r'^account/password/$', password_form, name='password_form'),
	url(r'^account/picture/$', picture_form, name='picture_form'),
	url(r'^account/social/$', social_form, name='social_form'),
	url(r'^account/services/$', services_form, name='services_form'),
	url(r'^article/add/$', add_article_form, name='add_article_form'),
	url(r'^article/edit/$', modify_article_form, name='modify_article_form'),
	url(r'^article/edit/(?P<postID>\d+)/$', modify_article_listing, name='modify_article_listing'),
	url(r'^article/delete/$', delete_article_listing, name='delete_article_listing'),
	url(r'^contact/$', contact_form, name='contact_form'),
	#url(r'^edit_profile/social/$', update_social_links, name='update_social_links'),
	#url(r'^edit_profile/password/$', update_password, name='update_password'),
	#url(r'^edit_profile/info/$', update_info, name='update_info'),
	#url(r'^edit_profile/photo/$', update_photo, name='update_info'),
	#url(r'^add/ajax/$', add_form_ajax, name='add_ajax'),
	#url(r'^add/$', add_form, name='add'),
	#url(r'^modify/(?P<postID>\d+)/ajax/$', modify_form_ajax, name='modify_ajax'),
	#url(r'^modify/(?P<postID>\d+)/$', modify_form, name='modify_listing'),
	#url(r'^modify/$', modify_listing, name='modify_listing'),
	#url(r'^delete/ajax/$', delete_ajax, name='delete_ajax'),
	#url(r'^delete/$', delete_listing, name='delete_listing'),
	#url(r'^tags/json/$', tags_ajax_json, name='add_ajax'),
	#url(r'^dev/$', index_dev, name='index_dev'),
]

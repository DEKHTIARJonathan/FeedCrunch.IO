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
	url(r'^account/preferences/$', preferences_form, name='preferences_form'),
	url(r'^account/password/$', password_form, name='password_form'),
	url(r'^account/picture/$', picture_form, name='picture_form'),
	url(r'^account/picture/upload/$', upload_picture, name='upload_picture'),
	url(r'^account/social/$', social_form, name='social_form'),
	url(r'^account/services/$', services_form, name='services_form'),
	url(r'^article/add/$', add_article_form, name='add_article_form'),
	url(r'^article/edit/$', modify_article_listing, name='modify_article_form'),
	url(r'^article/edit/(?P<postID>\d+)/$', modify_article_form, name='modify_article_listing'),
	url(r'^article/delete/$', delete_article_listing, name='delete_article_listing'),
	url(r'^reading/subscription/$', sub_management, name='sub_management'),
	url(r'^reading/recommendation/$', reading_recommendation, name='reading-recommendation'),
	url(r'^reading/recommendation/redirect/(?P<postID>\d+)/$', redirect_recommendation, name='redirect-recommendation'),
	url(r'^contact/$', contact_form, name='contact_form'),
]

# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.conf import settings

#from .admin import admin_site
from .views import *

urlpatterns = [
	url(r'^$', index, name='index'),
	url(r'^edit_profile/social/$', social_links_edit, name='social_links_edit'),
	url(r'^add/ajax/$', add_form_ajax, name='add_ajax'),
	url(r'^add/$', add_form, name='add'),
	url(r'^modify/(?P<postID>\d+)/ajax/$', modify_form_ajax, name='modify_ajax'),
	url(r'^modify/(?P<postID>\d+)/$', modify_form, name='modify_listing'),
	url(r'^modify/$', modify_listing, name='modify_listing'),
	url(r'^delete/ajax/$', delete_ajax, name='delete_ajax'),
	url(r'^delete/$', delete_listing, name='delete_listing'),
]

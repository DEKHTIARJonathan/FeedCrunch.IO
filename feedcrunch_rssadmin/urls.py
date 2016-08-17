# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.conf import settings

#from .admin import admin_site
from .views import *

urlpatterns = [
	url(r'^$', index, name='index'),
	url(r'^edit_profile/social/$', update_social_links, name='update_social_links'),
	url(r'^edit_profile/password/$', update_password, name='update_password'),
	url(r'^edit_profile/info/$', update_info, name='update_info'),
	url(r'^edit_profile/photo/$', update_photo, name='update_info'),
	url(r'^add/ajax/$', add_form_ajax, name='add_ajax'),
	url(r'^add/$', add_form, name='add'),
	url(r'^modify/(?P<postID>\d+)/ajax/$', modify_form_ajax, name='modify_ajax'),
	url(r'^modify/(?P<postID>\d+)/$', modify_form, name='modify_listing'),
	url(r'^modify/$', modify_listing, name='modify_listing'),
	url(r'^delete/ajax/$', delete_ajax, name='delete_ajax'),
	url(r'^delete/$', delete_listing, name='delete_listing'),
	url(r'^tags/json/$', tags_ajax_json, name='add_ajax'),
]

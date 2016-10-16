#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
import django.contrib.auth.views

#from .admin import admin_site
from .views import *

urlpatterns = [
	url(r'^$', index, name='index'),
	url(r'^faq/$', faq, name='faq'),
	url(r'^contact/$', contact, name='contact'),
	url(r'^about/$', about, name='about'),
	url(r'^login/$', loginView, name='login'),
	url(r'^signup/$', signUPView, name='signup'),
	url(r'^terms/$', terms, name='terms'),
	url(r'^logout/$', django.contrib.auth.views.logout, {'next_page': '/login',}, name='logout'),
]

if settings.DEBUG:
	urlpatterns.append(url(r'^media/(?P<path>.*)$', django.views.static.serve, {'document_root': settings.MEDIA_ROOT}))

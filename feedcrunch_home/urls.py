#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import url

from django.conf import settings
import django.contrib.auth.views
import django.views.static

from feedcrunch_home.views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^faq/$', faq, name='faq'),
    url(r'^contact/$', contact, name='contact'),
    url(r'^about/$', about, name='about'),
    url(r'^login/$', loginView, name='login'),
    url(r'^signup/$', signUPView, name='signup'),
    url(r'^terms/$', terms, name='terms'),
    url(r'^logout/$', django.contrib.auth.views.LogoutView.as_view(), {'next_page': '/login',}, name='logout'),
]

if settings.DEBUG or settings.TESTING:
    urlpatterns.append(url(r'^media/(?P<path>.*)$', django.views.static.serve, {'document_root': settings.MEDIA_ROOT}))

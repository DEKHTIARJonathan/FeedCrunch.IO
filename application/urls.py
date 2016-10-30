#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
"""application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.conf.urls import url, include
	2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()

# Examples:
# url(r'^$', 'settings.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
	#url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
	url(r'^admin/', include(admin.site.urls)),
	url(r'^api/1.0/', include('feedcrunch_api_v1.urls')),
	url(r'', include('feedcrunch_home.urls')),
	url(r'^twitter/oauth/', include('twitter.urls')),
	url(r'^@(?P<feedname>\w+)/admin/', include('feedcrunch_rssadmin.urls')),
	url(r'^@(?P<feedname>\w+)/admin_dev/', include('feedcrunch_rssadmin_dev.urls')),
	url(r'^@(?P<feedname>\w+)/', include('feedcrunch_rssviewer.urls')),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
	#url(r'^$', feedcrunch_home.views.index, name='index'),
]

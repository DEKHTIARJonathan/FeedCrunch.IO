# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.conf import settings

#from .admin import admin_site
from .views import *

urlpatterns = [
	url(r'^get_callback/$', get_callback, name='get_callback'),
	url(r'^unlink/$', unlink, name='unlink'),
]

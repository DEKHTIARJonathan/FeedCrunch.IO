from django.conf.urls import include, url
from django.conf import settings

#from .admin import admin_site
from .views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^add/ajax/', admin_add_ajax, name='add_ajax'),
    url(r'^add/', admin_add, name='add'),
]

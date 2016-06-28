from django.conf.urls import include, url
from django.conf import settings

#from .admin import admin_site
from .views import index

urlpatterns = [
    url(r'^$', index, name='index'),
]

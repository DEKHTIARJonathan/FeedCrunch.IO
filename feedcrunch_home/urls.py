from django.conf.urls import include, url
from django.conf import settings

#from .admin import admin_site
from .views import index, faq, contact, about

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^faq/', faq, name='faq'),
    url(r'^contact/', contact, name='contact'),
    url(r'^about/', about, name='contact'),
]

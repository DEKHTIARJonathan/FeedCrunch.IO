#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

from .models_user import FeedUser

from ipware.ip import get_ip
############################# Subscribtion #####################################

# First, define the Manager subclass.
class SubManager(models.Manager):
    def create(self, request, feedname=None):

        try:
            if feedname == None:
                raise Exception("Feedname is missing")

            ip = get_ip(request, right_most_proxy=True)
            usr = FeedUser.objects.get(username=feedname) # If fails, raise an Exception

            if ip is None:
                # we don't have an ip address for user
                raise Exception("There had been a problem retrieving the IP address for the user.")

            return super(SubManager, self).create(user=usr, ipaddress=ip)

        except Exception as e:
            #return {'status': False, 'error': str(e)}
            return False


# Then the Model Class
class RSSSubscriber(models.Model):

    objects = SubManager()

    user = models.ForeignKey(FeedUser, related_name='rel_rss_subscribers')
    ipaddress = models.GenericIPAddressField(protocol='both', unpack_ipv4=False)
    when = models.DateTimeField(auto_now_add=True, primary_key=True)

    def __str__(self):
        return self.ipaddress + " // " + str(self.when)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from .models_user import FeedUser

from djchoices import DjangoChoices, ChoiceItem

from ipware.ip import get_real_ip, get_ip

import datetime

######################################## Subscribtion ################################################

# First, define the Manager subclass.
class SubManager(models.Manager):
    def create(self, request, feedtype, feedname=None):

        try:
            if feedname == None:
                raise Exception("Feedname is missing")

            ipaddr = get_real_ip(request)

            if ipaddr is None:
                ipaddr = get_ip(request)

                if ipaddr is None:
                    raise Exception("There had been a problem retrieving the IP address for the user.")

            usr = FeedUser.objects.get(username=feedname) # If fails, raise an Exception
            return super(SubManager, self).create(user=usr, ipaddress=ipaddr, feedtype=feedtype, visit_hour=timezone.now().hour)

        except Exception as e:
            #return {'status': False, 'error': str(e)}
            return None

# Then the Model Class
class RSSSubscriber(models.Model):

    objects = SubManager()

    # Choices
    class FeedType(DjangoChoices):
        rss = ChoiceItem()
        atom = ChoiceItem()
        web = ChoiceItem()

    id         = models.AutoField(primary_key=True)
    user       = models.ForeignKey(FeedUser, related_name='rel_rss_subscribers')
    ipaddress  = models.GenericIPAddressField(protocol='both', unpack_ipv4=False)
    date       = models.DateField(auto_now_add=True, blank=False, null=False)
    feedtype   = models.CharField(max_length=4, choices=FeedType.choices, default=FeedType.rss)
    visit_hour = models.SmallIntegerField(default=0, validators=[ MaxValueValidator(23), MinValueValidator(0)], blank=False, null=False)

    def __str__(self):
        return self.ipaddress + " // " + str(self.date)

##################################### Subscribtion Statistics #############################################

class RSSSubsStat(models.Model):

    id    = models.AutoField(primary_key=True)
    user  = models.ForeignKey(FeedUser, related_name='rel_rss_subscribers_count', blank=False, null=False)
    date  = models.DateField(auto_now_add=True, blank=False, null=False)
    count = models.IntegerField(default=0, blank=False, null=False)

    class Meta:
        unique_together = ('user', 'date')

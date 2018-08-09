#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .models_user import FeedUser

from djchoices import DjangoChoices, ChoiceItem

from ipware.ip import get_real_ip, get_ip

import datetime

######################################## Subscription ################################################


# First, define the Manager subclass.
class SubManager(models.Manager):
    def create(self, request, feedtype, feedname=None):

        try:
            if feedname is None:
                raise Exception("Feedname is missing")

            ipaddr = get_real_ip(request)

            if ipaddr is None:
                ipaddr = get_ip(request)

                if ipaddr is None:
                    raise Exception("There had been a problem retrieving the IP address for the user.")

            usr = FeedUser.objects.get(username=feedname) # If fails, raise an Exception
            return super(SubManager, self).create(user=usr, ipaddress=ipaddr, feedtype=feedtype, visit_hour=datetime.datetime.now().hour)

        except Exception as e:
            #return {'status': False, 'error': str(e)}
            return None


# Then the Model Class
class RSSSubscriber(models.Model):

    objects = SubManager()

    # Choices
    class FeedType(DjangoChoices):
        rss  = ChoiceItem()
        atom = ChoiceItem()
        web  = ChoiceItem()

    id         = models.AutoField(primary_key=True)
    user       = models.ForeignKey(FeedUser, related_name='rel_rss_subscribers', on_delete=models.CASCADE)
    ipaddress  = models.GenericIPAddressField(protocol='both', unpack_ipv4=False)
    date       = models.DateField(auto_now_add=True, blank=False, null=False)
    feedtype   = models.CharField(max_length=4, choices=FeedType.choices, default=FeedType.rss)
    visit_hour = models.SmallIntegerField(default=0, validators=[ MaxValueValidator(23), MinValueValidator(0)], blank=False, null=False)

    def __str__(self):
        return self.ipaddress + " // " + str(self.date)


##################################### subscription Statistics #############################################

# First, define the Manager subclass.
class RSSSubsStatManager(models.Manager):
    def create(self, user=None, count=0, date=None):
        try:
            if user is None:
                raise Exception("Feedname is missing")

            elif isinstance(user, str):
                user = FeedUser.objects.get(username=user) # If fails, raise an Exception

            if date is None:
                date = datetime.datetime.now().date() - datetime.timedelta(days=1)

            return super(RSSSubsStatManager, self).create(user=user, count=count, date=date)

        except Exception as e:
            return {'status': False, 'error': str(e), 'timestamp': datetime.datetime.now()}


class RSSSubsStat(models.Model):

    objects = RSSSubsStatManager()

    id    = models.AutoField(primary_key=True)
    user  = models.ForeignKey(FeedUser, related_name='rel_rss_subscribers_count', blank=False, null=False, on_delete=models.CASCADE)
    date  = models.DateField(auto_now_add=False, blank=False, null=False)
    count = models.IntegerField(default=0, blank=False, null=False)

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return self.user.username + " (" + str(self.date) + "): " + str(self.count)

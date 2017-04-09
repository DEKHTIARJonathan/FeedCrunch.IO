#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

#from django.db import models
#
#
#from django.core.exceptions import ObjectDoesNotExist
#
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

from django_q.tasks import schedule
from django_q.models import Schedule

from feedcrunch.models import FeedUser #, RSSFeed, RSSSubscriber, RSSSubsStat

from datetime import timedelta


def send_mass_welcome_email():
    for user in FeedUser.objects.all():
        schedule('feedcrunch.tasks.send_welcome_email', username=user.username, schedule_type=Schedule.ONCE, next_run=timezone.now() + timedelta(minutes=1))

def send_welcome_email(username):
    usr = FeedUser.objects.get(username=username)

    msg_plain = render_to_string('emails/welcome.txt', {'firstname': usr.get_short_name()})
    msg_html = render_to_string('emails/welcome.html', {'firstname': usr.get_short_name()})

    send_mail(
        'Welcome at Feedcrunch.io - Start sharing your expertise with the world',
        msg_plain,
        settings.AWS_SES_SENDER,
        [usr.email],
        html_message=msg_html,
    )

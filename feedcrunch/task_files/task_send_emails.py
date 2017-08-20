#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from application.celery import app as celery
#
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from feedcrunch import models
from feedcrunch.models import FeedUser #, RSSFeed, RSSSubscriber, RSSSubsStat

def send_mass_welcome_email():
    for user in FeedUser.objects.all():
        send_welcome_email.delay(username=user.username)

@celery.task(name='feedcrunch.tasks.send_welcome_email')
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

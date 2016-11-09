# Welcome mail with follow up example
from datetime import timedelta
from django.utils import timezone
from django_q.tasks import async, schedule
from django_q.models import Schedule
from django.conf import settings

def welcome_mail(user):
  msg = 'Welcome to our website'
  # send this message right away
  async('django.core.mail.send_mail',
        'Welcome',
         msg,
         settings.EMAIL_HOST_USER,
         [user.email])
  # and this follow up email in one hour
  msg = 'Here are some tips to get you started...'
  schedule('django.core.mail.send_mail',
       'Follow up',
       msg,
       settings.EMAIL_HOST_USER,
       [user.email],
       schedule_type=Schedule.ONCE,
       next_run=timezone.now() + timedelta(minutes=1))

  # since the `repeats` defaults to -1
  # this schedule will erase itself after having run


def check_rss_subscribtion(username):
	from feedcrunch.models import FeedUser
	usr = FeedUser.objects.get(username=username)
	usr.check_rss_subscribtion()

"""
from feedcrunch.models import FeedUser
a = FeedUser.objects.get(username="dataradar")
welcome_mail(a)
"""
schedule('check_rss_subscribtion', 'dataradar', schedule_type=Schedule.ONCE, next_run=timezone.now() + timedelta(minutes=1))

# Welcome mail with follow up example
from datetime import timedelta
from django.utils import timezone
from django_q.tasks import async, schedule
from django_q.models import Schedule
from django.conf import settings

def welcome_mail(username):
  from feedcrunch.models import FeedUser
  user = FeedUser.objects.get(username=username)
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


def check_allUsers_rss_subscribtions():
	from feedcrunch.models import FeedUser
	user_list = FeedUser.objects.all()

	for user in user_list:
		schedule('feedcrunch.tasks.check_rss_subscribtion', username=user.username, schedule_type=Schedule.ONCE, next_run=timezone.now() + timedelta(minutes=1))


def launch_recurrent_tasks():
	execution_time = timezone.now()
	execution_time = execution_time.replace(hour=3, minute=0, second=0, microsecond=0) + timedelta(days=1)
	schedule('feedcrunch.tasks.check_allUsers_rss_subscribtions', schedule_type=Schedule.DAILY, next_run=execution_time)

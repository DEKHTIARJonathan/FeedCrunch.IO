# Welcome mail with follow up example
from datetime import timedelta
from django.utils import timezone
from django_q.tasks import async, schedule
from django_q.models import Schedule
from django.conf import settings

from django.core.mail import send_mail

from feedcrunch.models import FeedUser, RSSFeed

from django.core.mail import send_mail
from django.template.loader import render_to_string

def welcome_mail(username):
	user = FeedUser.objects.get(username=username)
	msg = 'Welcome to our website'
	# send this message right away
	async('django.core.mail.send_mail',
		'Welcome',
		msg,
		settings.EMAIL_HOST_USER,
		[user.email]
	)
	# and this follow up email in one hour

	msg = 'Here are some tips to get you started...'
	send_mail(
		'Follow up',
		msg,
		settings.EMAIL_HOST_USER,
		[user.email]
	)
	"""
	schedule('django.core.mail.send_mail',
		'Follow up',
		msg,
		settings.EMAIL_HOST_USER,
		[user.email],
		schedule_type=Schedule.ONCE,
		next_run=timezone.now() + timedelta(minutes=1)
	)
	"""

  # since the `repeats` defaults to -1
  # this schedule will erase itself after having run

def check_rss_feed(rss_id):
	feed = RSSFeed.objects.get(id=rss_id)
	feed.refresh_feed()

def check_user_rss_subscribtions(username):
	usr = FeedUser.objects.get(username=username)

	for feed in usr.rel_feeds.filter(active=True):
		schedule('feedcrunch.tasks.check_rss_feed', rss_id=feed.id, schedule_type=Schedule.ONCE, next_run=timezone.now() + timedelta(minutes=1))

def check_allUsers_rss_subscribtions():
	for user in FeedUser.objects.all():
		schedule('feedcrunch.tasks.check_user_rss_subscribtions', username=user.username, schedule_type=Schedule.ONCE, next_run=timezone.now() + timedelta(minutes=1))

def launch_recurrent_rss_job():
	execution_time = timezone.now()
	execution_time = execution_time.replace(hour=3, minute=0, second=0, microsecond=0) + timedelta(days=1)

	schedule('feedcrunch.tasks.check_allUsers_rss_subscribtions', schedule_type=Schedule.HOURLY, next_run=execution_time)

def send_mass_welcome_email():
	for user in FeedUser.objects.all():
		send_welcome_email(user.username)

def send_welcome_email(user_name):
	usr = FeedUser.objects.get(username=user_name)

	msg_plain = render_to_string('emails/welcome.html', {'firstname': usr.get_short_name()})
	msg_html = render_to_string('emails/welcome.html', {'firstname': usr.get_short_name()})

	send_mail(
		'Welcome at Feedcrunch.io - Start sharing your expertise with the world',
		msg_plain,
		settings.AWS_SES_SENDER,
		[usr.email],
		html_message=msg_html,
	)

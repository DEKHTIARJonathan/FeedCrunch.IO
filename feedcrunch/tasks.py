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
	RSSFeed.objects.get(id=rss_id).refresh_feed()

def refresh_user_rss_subscribtions(username):
	for feed in RSSFeed.objects.filter(rel_sub_feed_assoc__user=username):
		schedule('feedcrunch.tasks.check_rss_feed', rss_id=feed.id, schedule_type=Schedule.ONCE, next_run=timezone.now() + timedelta(minutes=1))

def refresh_all_rss_feeds():
	for feed in RSSFeed.objects.all():
		schedule('feedcrunch.tasks.check_rss_feed', rss_id=feed.id, schedule_type=Schedule.ONCE, next_run=timezone.now() + timedelta(minutes=1))

def launch_recurrent_rss_job():
	execution_time = timezone.now()
	execution_time = execution_time.replace(hour=3, minute=0, second=0, microsecond=0) + timedelta(days=1)

	schedule('feedcrunch.tasks.refresh_all_rss_feeds', schedule_type=Schedule.HOURLY, next_run=execution_time)

def send_mass_welcome_email():
	for user in FeedUser.objects.all():
		send_welcome_email(user.username)

def send_welcome_email(user_name):
	usr = FeedUser.objects.get(username=user_name)

	msg_plain = render_to_string('emails/welcome.txt', {'firstname': usr.get_short_name()})
	msg_html = render_to_string('emails/welcome.html', {'firstname': usr.get_short_name()})

	send_mail(
		'Welcome at Feedcrunch.io - Start sharing your expertise with the world',
		msg_plain,
		settings.AWS_SES_SENDER,
		[usr.email],
		html_message=msg_html,
	)

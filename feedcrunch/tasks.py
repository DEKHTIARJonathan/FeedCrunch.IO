# Welcome mail with follow up example
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from django_q.tasks import async, schedule
from django_q.models import Schedule

from feedcrunch.models import FeedUser, RSSFeed, RSSSubscriber, RSSSubsStat

from datetime import timedelta, date

########################################################## REFRESH RSS FEEDS ##########################################################

def check_rss_feed(rss_id):
    RSSFeed.objects.get(id=rss_id).refresh_feed()

def refresh_user_rss_subscribtions(username=None):
    if username is not None:
        for feed in RSSFeed.objects.filter(rel_sub_feed_assoc__user=username):
            schedule('feedcrunch.tasks.check_rss_feed', rss_id=feed.id, schedule_type=Schedule.ONCE, next_run=timezone.now() + timedelta(minutes=1))
    else:
        raise Exception("Error: tasks.refresh_user_rss_subscribtions - username have not been provided.")

def refresh_all_rss_feeds():
    for feed in RSSFeed.objects.all():
        schedule('feedcrunch.tasks.check_rss_feed', rss_id=feed.id, schedule_type=Schedule.ONCE, next_run=timezone.now() + timedelta(minutes=1))

###################################################### REFRESH RSS SUBSCRIBERS COUNT  ##################################################

def record_user_subscribtions_stats(username=None):
    if username is not None:

        today           = date.today()
        sub_timedelta   = settings.RSS_SUBS_LOOKUP_PERIOD
        last_lookup_day = today - timedelta(days=sub_timedelta)

        usr   = FeedUser.objects.get(username=username)

        if not usr.rel_rss_subscribers_count.filter(date=date.today()).exists(): # Check if a statistic already exists for that day

            #count = usr.rel_rss_subscribers.filter(date__range=(last_lookup_day, today)).values("ipaddress").annotate(n=models.Count("pk")).count()__gte
            count = usr.rel_rss_subscribers.filter(date__gte=last_lookup_day).values("ipaddress").annotate(n=models.Count("pk")).count()

            stat_obj = RSSSubsStat(user=usr, count=count)
            stat_obj.save()

    else:
        raise Exception("Error: tasks.record_user_subscribtions_stats - username have not been provided.")

def refresh_all_rss_subscribers_count():
    for user in FeedUser.objects.all():
        schedule('feedcrunch.tasks.record_user_subscribtions_stats', username=user.username, schedule_type=Schedule.ONCE, next_run=timezone.now() + timedelta(minutes=1))

########################################################## SEND WELCOME EMAIL  ##########################################################

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

########################################################## LAUNCH RECURRING JOB  ##########################################################

def launch_recurrent_rss_job():
    execution_time = timezone.now()
    execution_time = execution_time.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)

    schedule('feedcrunch.tasks.refresh_all_rss_feeds', schedule_type=Schedule.HOURLY, next_run=execution_time)
    schedule('feedcrunch.tasks.refresh_all_rss_subscribers_count', schedule_type=Schedule.DAILY, next_run=execution_time)

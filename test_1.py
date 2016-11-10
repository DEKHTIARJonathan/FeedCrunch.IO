# Welcome mail with follow up example
from datetime import timedelta
from django.utils import timezone
from django_q.tasks import schedule
from django_q.models import Schedule

schedule('feedcrunch.tasks.check_rss_subscribtion', username='dataradar', schedule_type=Schedule.ONCE, next_run=timezone.now() + timedelta(minutes=1))

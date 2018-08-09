#!/usr/bin/env python
# -*- coding: utf-8 -*-

# noinspection PyUnresolvedReferences
from feedcrunch.task_files import *
from feedcrunch.task_files import __all__ as __all__tasks__

__all__ = __all__tasks__

####################################################################################################################
# ============================================ LAUNCH RECURRING JOB  ============================================= #
####################################################################################################################

'''
def launch_recurrent_rss_job():
    execution_time = datetime.datetime.now()
    execution_time = execution_time.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)

    schedule('feedcrunch.tasks.refresh_all_rss_feeds', schedule_type=Schedule.HOURLY, next_run=execution_time)
    schedule('feedcrunch.tasks.refresh_all_rss_subscribers_count', schedule_type=Schedule.DAILY, next_run=execution_time)
'''

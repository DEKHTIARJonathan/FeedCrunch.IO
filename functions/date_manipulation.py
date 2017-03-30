#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals


import datetime as DT
from django.utils import timezone


def get_N_time_period(N_periods=14, duration=1, max_date=DT.date.today()):

    d_today = timezone.now()
    max_date_delta = (d_today.date()-max_date).days

    delta = 1
    while N_periods * delta < max_date_delta and delta < duration:
        delta += 1

    rslt = []

    for d in range(0, N_periods):
        rslt.append(timezone.make_aware(d_today - DT.timedelta(days=d*delta+1), timezone.get_current_timezone()))

    rslt.reverse() #From the oldest day to the most recent

    return rslt

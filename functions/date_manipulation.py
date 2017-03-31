#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals


import datetime


def get_N_time_period(N_periods=14, duration=1, max_date=datetime.date.today()):

    d_today = datetime.datetime.now()
    max_date_delta = (d_today.date()-max_date).days

    delta = 1
    while N_periods * delta < max_date_delta and delta < duration:
        delta += 1

    rslt = []

    for d in range(0, N_periods):
        rslt.append(d_today - datetime.timedelta(days=d*delta+1))

    rslt.reverse() #From the oldest day to the most recent

    return rslt

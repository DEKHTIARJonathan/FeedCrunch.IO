#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals


import datetime as DT
from django.utils import timezone


def get_N_time_period(N_periods=14, duration=1):

	d_today = DT.datetime.now()

	delta = DT.timedelta(days=duration)

	rslt = []

	for d in range(1, N_periods + 1):
		rslt.append(timezone.make_aware(d_today - DT.timedelta(days=d*duration), timezone.get_current_timezone()))

	rslt.reverse() #From the oldest day to the most recent

	return rslt

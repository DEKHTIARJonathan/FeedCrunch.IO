#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import JsonResponse

from feedcrunch.models import Post, FeedUser

import datetime, time
# Create your views here.

def get_timestamp():
	return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

def validate_username(request, username=None):

	payload = dict()

	if username == None:
		payload ["success"] = False
		payload ["error"] = "Username not provided"

	else:
		payload ["success"] = True
		payload ["exist"] = FeedUser.objects.filter(username = username).exists()

	payload ["timestamp"] = get_timestamp()

	return JsonResponse(payload, safe=False)

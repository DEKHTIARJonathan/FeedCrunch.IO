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

	username_get = request.GET.get('username')

	if request.method != 'GET':
		payload ["success"] = False
		payload ["error"] = "Only GET Requests accepted"

	elif username == None and username_get == None:
		payload ["success"] = False
		payload ["error"] = "Username not provided"

	else:
		payload ["success"] = True
		if username == None:
			payload ["username"] = username_get
		else :
			payload ["username"] = username

		payload ["available"] = not FeedUser.objects.filter(username = payload ["username"]).exists()

	payload ["timestamp"] = get_timestamp()

	return JsonResponse(payload, safe=False)

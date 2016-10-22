#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import JsonResponse

from feedcrunch.models import Post, FeedUser

from check_admin import check_admin
from time_funcs import get_timestamp
from date_manipulation import get_N_time_period

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

def publications_stats(request, feedname=None):
	check_passed = check_admin(feedname, request.user)
	if check_passed != True:
		return check_passed
	else:

		payload = dict()

		if request.method != 'GET':
			payload ["success"] = False
			payload ["error"] = "Only GET Requests accepted"

		else:
			payload ["success"] = True
			payload ["username"] = feedname

			user = FeedUser.objects.get(username=feedname)

			date_array = get_N_time_period(21)

			ticks = []
			data = []

			for i, d in enumerate(date_array):

				count = user.rel_posts.filter(when__year=d.year, when__month=d.month, when__day=d.day).count()
				data.append([i, count])
				ticks.append([i, d.strftime("%d. %b")])

			payload ["data"] = data
			payload ["ticks"] = ticks

		payload ["timestamp"] = get_timestamp()

		return JsonResponse(payload, safe=False)

def subscribers_stats(request, feedname=None):
	check_passed = check_admin(feedname, request.user)
	if check_passed != True:
		return check_passed
	else:

		payload = dict()

		if request.method != 'GET':
			payload ["success"] = False
			payload ["error"] = "Only GET Requests accepted"

		else:
			payload ["success"] = True
			payload ["username"] = feedname

			user = FeedUser.objects.get(username=feedname)

			date_array = get_N_time_period(21, 14)

			ticks = []
			data = []

			from random import randint

			for i, d in enumerate(date_array):

				#count = user.rel_posts.filter(when__year=d.year, when__month=d.month, when__day=d.day).count()
				#data.append([i, count])
				data.append([i, randint(5000,12000)])
				ticks.append([i, d.strftime("%d. %b")])

			payload ["data"] = data
			payload ["ticks"] = ticks

		payload ["timestamp"] = get_timestamp()

		return JsonResponse(payload, safe=False)

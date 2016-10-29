#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import JsonResponse

from feedcrunch.models import Post, FeedUser, Tag

from twitter.tw_funcs import TwitterAPI, get_authorization_url

import datetime, unicodedata, json, sys, os

from check_admin import check_admin_api
from time_funcs import get_timestamp
from date_manipulation import get_N_time_period
from data_convert import str2bool
from ap_style import format_title

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

def publications_stats(request):
	payload = dict()
	check_passed = check_admin_api(request.user)

	if request.method != 'GET':
			payload ["success"] = False
			payload ["error"] = "Only GET Requests accepted"

	elif check_passed != True:
		payload ["success"] = False
		payload ["error"] = check_passed

	else:
		feedname = request.user.username
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

def subscribers_stats(request):
	payload = dict()
	check_passed = check_admin_api(request.user)

	if request.method != 'GET':
			payload ["success"] = False
			payload ["error"] = "Only GET Requests accepted"

	elif check_passed != True:
		payload ["success"] = False
		payload ["error"] = check_passed

	else:

		feedname = request.user.username
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

	from time import sleep
	sleep(3)

	payload ["timestamp"] = get_timestamp()
	return JsonResponse(payload, safe=False)

def tags_as_json(request):
	payload = dict()
	check_passed = check_admin_api(request.user)

	if request.method != 'GET':
			payload ["success"] = False
			payload ["error"] = "Only GET Requests accepted"

	elif check_passed != True:
		payload ["success"] = False
		payload ["error"] = check_passed

	else:
		payload ["success"] = True
		payload ["username"] = request.user.username

		tags = Tag.objects.all().order_by('name')
		payload["tags"] = [tag.name for tag in tags]


	payload ["timestamp"] = get_timestamp()
	return JsonResponse(payload, safe=False)

def submit_article(request):
	try:
		payload = dict()
		check_passed = check_admin_api(request.user)

		if request.method != 'POST':
				payload ["success"] = False
				payload ["error"] = "Only POST Requests accepted"

		elif check_passed != True:
			payload ["success"] = False
			payload ["error"] = check_passed

		else:
			payload ["username"] = request.user.username


			title = unicodedata.normalize('NFC', request.POST['title'])
			link = unicodedata.normalize('NFC', request.POST['link'])
			tags = unicodedata.normalize('NFC', request.POST['tags']).split(',') # We separate each tag and create a list out of it.

			activated_bool = str2bool(unicodedata.normalize('NFC', request.POST['activated']))
			twitter_bool = str2bool(unicodedata.normalize('NFC', request.POST['twitter']))

			if str2bool(unicodedata.normalize('NFC', request.POST['autoformat'])) :
				title = format_title(title)

			if title == "" or link == "":
				payload["success"] = False
				payload["error"] = "Title and/or Link is/are missing"

			else:

				tmp_user = FeedUser.objects.get(username=request.user.username)
				tmp_post = Post.objects.create(title=title, link=link, clicks=0, user=tmp_user, activeLink=activated_bool)

				for tag in tags:
					tmp_obj, created_bool = Tag.objects.get_or_create(name=tag)
					tmp_post.tags.add(tmp_obj)
				tmp_post.save()

				if twitter_bool and tmp_user.is_twitter_enabled():

						twitter_instance = TwitterAPI(tmp_user)

						if twitter_instance.connection_status():
							tmp_post.save()

							tw_rslt = twitter_instance.post_twitter(title, tmp_post.id, tags)

							if not tw_rslt['status']:
								payload["success"] = False
								payload["postID"] = str(tmp_post.id)
								payload["error"] = "An error occured in the twitter posting process, but the post was saved: " + tw_rslt['error']

							else:
								payload["success"] = True
								payload["postID"] = str(tmp_post.id)

						else:
							raise Exception("Not connected to the Twitter API")

				else:
					tmp_post.save()
					payload["success"] = True
					payload["postID"] = str(tmp_post.id)

	except Exception, e:
		payload["status"] = "error"
		payload["error"] = "An error occured in the process: " + str(e)
		payload["postID"] = None

	payload["operation"] = "submit article"
	payload ["timestamp"] = get_timestamp()
	return JsonResponse(payload, safe=False)

def modify_article(request, postID=None):
	try:
		payload = dict()
		check_passed = check_admin_api(request.user)

		if request.method != 'POST':
			raise Exception("Only POST Requests accepted")

		if type(postID) is not int or postID < 1:
			raise Exception("postID parameter is not valid")

		if check_passed != True:
			raise Exception(check_passed)
		else:
			feedname = request.user.username
			payload ["username"] = request.user.username

		title = unicodedata.normalize('NFC', request.POST['title'])
		link = unicodedata.normalize('NFC', request.POST['link'])

		if title == "" or link == "":
			raise Exception("Title and/or Link is/are missing")

		tags = unicodedata.normalize('NFC', request.POST['tags']).split(',') # We separate each tag and create a list out of it.

		activated_bool = str2bool(unicodedata.normalize('NFC', request.POST['activated']))
		twitter_bool = str2bool(unicodedata.normalize('NFC', request.POST['twitter']))

		if str2bool(unicodedata.normalize('NFC', request.POST['autoformat'])) :
			title = format_title(title)


		tmp_post = Post.objects.get(id=postID, user=feedname)

		tmp_post.title = title
		tmp_post.link = link
		tmp_post.activeLink = activated_bool
		tmp_post.tags.clear()

		for tag in tags:
			tmp_obj, created_bool = Tag.objects.get_or_create(name=tag)
			tmp_post.tags.add(tmp_obj)

		tmp_user = FeedUser.objects.get(username=feedname)

		if twitter_bool and tmp_user.is_twitter_enabled():

			twitter_instance = TwitterAPI(tmp_user)

			if twitter_instance.connection_status():
				tmp_post.save()

				tw_rslt = twitter_instance.post_twitter(title, tmp_post.id, tags)

				if not tw_rslt['status']:
					payload["postID"] = str(tmp_post.id)
					raise Exception("Twitter posting error, however the post was saved: " + tw_rslt['error'])

			else:
				raise Exception("Not connected to the Twitter API")

		tmp_post.save()
		payload["success"] = True
		payload["postID"] = str(postID)

	except Exception, e:
		payload["success"] = False
		payload["error"] = "An error occured in the process: " + str(e)
		payload["postID"] = None


	payload["operation"] = "modify article"
	payload ["timestamp"] = get_timestamp()
	return JsonResponse(payload, safe=False)

def delete_article (request, postID=None):
	try:
		payload = dict()
		check_passed = check_admin_api(request.user)

		if request.method != "DELETE":
			raise Exception("Only DELETE Requests accepted")

		postID = int(unicodedata.normalize('NFC', postID))
		if type(postID) is not int or postID < 1:
			raise Exception("postID parameter is not valid")

		if check_passed != True:
			raise Exception(check_passed)

		feedname = request.user.username
		payload ["username"] = request.user.username

		post = Post.objects.filter(id=postID, user=feedname)
		if post.count() == 0:
			raise Exception("Post does not exist")

		post.delete()
		payload ["success"] = True
		payload["postID"] = postID

	except Exception, e:
		payload["success"] = False
		payload["error"] = "An error occured in the process: " + str(e)
		payload["postID"] = None

	payload ["operation"] = "delete article"
	payload ["timestamp"] = get_timestamp()
	return JsonResponse(payload, safe=False)

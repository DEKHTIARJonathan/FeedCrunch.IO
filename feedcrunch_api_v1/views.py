#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from rest_framework.views import APIView
from rest_framework.response import Response

from feedcrunch.models import Post, FeedUser, Tag, Country

from twitter.tw_funcs import TwitterAPI, get_authorization_url

import datetime, unicodedata, json, sys, os

from check_admin import check_admin_api
from time_funcs import get_timestamp
from date_manipulation import get_N_time_period
from data_convert import str2bool
from ap_style import format_title

class Username_Validation(APIView):

	def get(self, request, username=None):

		try:

			payload = dict()
			username_get = request.GET.get('username')

			if username == None and username_get == None:
				raise Exception("Username not provided")

			else:

				if username == None:
					payload ["username"] = username_get
				else :
					payload ["username"] = username

				payload ["available"] = not FeedUser.objects.filter(username = payload ["username"]).exists()
				payload ["success"] = True

		except Exception, e:
			payload["success"] = False
			payload["error"] = "An error occured in the process: " + str(e)

		payload["operation"] = "Username Validation"
		payload ["timestamp"] = get_timestamp()
		return Response(payload)

class User_Stats_Subscribers(APIView):

	def get(self, request):
		try:

			payload = dict()
			check_passed = check_admin_api(request.user)

			if check_passed != True:
				raise Exception(check_passed)

			feedname = request.user.username
			payload ["success"] = True
			payload ["username"] = feedname

			date_array = get_N_time_period(21, 14)

			ticks = []
			data = []

			from random import randint

			for i, d in enumerate(date_array):

				#count = request.user.rel_posts.filter(when__year=d.year, when__month=d.month, when__day=d.day).count()
				#data.append([i, count])
				data.append([i, randint(5000,12000)])
				ticks.append([i, d.strftime("%d. %b")])

			payload ["data"] = data
			payload ["ticks"] = ticks

			from time import sleep
			sleep(3)

		except Exception, e:
			payload["success"] = False
			payload["error"] = "An error occured in the process: " + str(e)

		payload["operation"] = "Get User Publication Stats"
		payload ["timestamp"] = get_timestamp()
		return Response(payload)

class User_Stats_Publications(APIView):
	def get(self, request):
		try:

			payload = dict()
			check_passed = check_admin_api(request.user)

			if check_passed != True:
				raise Exception(check_passed)

			feedname = request.user.username
			payload ["success"] = True
			payload ["username"] = feedname

			date_array = get_N_time_period(21)

			ticks = []
			data = []

			for i, d in enumerate(date_array):

				count = request.user.rel_posts.filter(when__year=d.year, when__month=d.month, when__day=d.day).count()
				data.append([i, count])
				ticks.append([i, d.strftime("%d. %b")])

			payload ["data"] = data
			payload ["ticks"] = ticks

		except Exception, e:
			payload["success"] = False
			payload["error"] = "An error occured in the process: " + str(e)

		payload["operation"] = "Get User Subscriber Stats"
		payload ["timestamp"] = get_timestamp()
		return Response(payload)

class Tags(APIView):
	def get(self, request):
		try:

			payload = dict()
			check_passed = check_admin_api(request.user)

			if check_passed != True:
				raise Exception(check_passed)

			tags = Tag.objects.all().order_by('name')
			payload["tags"] = [tag.name for tag in tags]

			payload ["success"] = True
			payload ["username"] = request.user.username

		except Exception, e:
			payload["success"] = False
			payload["error"] = "An error occured in the process: " + str(e)

		payload["operation"] = "Get All Tags"
		payload ["timestamp"] = get_timestamp()
		return Response(payload)

class Article(APIView): # Add Article (POST), Get Article  (GET), Modify Article  (PUT), DELETE Article (DELETE)

	def get(self, request):
		payload = dict()
		payload["success"] = True
		return Response(payload)

	def post(self, request):
		try:
			payload = dict()
			check_passed = check_admin_api(request.user)

			if check_passed != True:
				raise Exception(check_passed)

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
					raise Exception("Title and/or Link is/are missing")


				tmp_user = FeedUser.objects.get(username=request.user.username)
				tmp_post = Post.objects.create(title=title, link=link, clicks=0, user=tmp_user, activeLink=activated_bool)

				for tag in tags:
					tmp_obj, created_bool = Tag.objects.get_or_create(name=tag)
					tmp_post.tags.add(tmp_obj)

				tmp_post.save()

				if twitter_bool and tmp_user.is_twitter_enabled():

						twitter_instance = TwitterAPI(tmp_user)

						if twitter_instance.connection_status():

							tw_rslt = twitter_instance.post_twitter(title, tmp_post.id, tags)

							if not tw_rslt['status']:
								payload["postID"] = str(tmp_post.id)
								raise Exception("An error occured in the twitter posting process, but the post was saved: " + tw_rslt['error'])

						else:
							raise Exception("Not connected to the Twitter API")

				payload["success"] = True
				payload["postID"] = str(tmp_post.id)

		except Exception, e:
			payload["success"] = False
			payload["error"] = "An error occured in the process: " + str(e)

		payload["operation"] = "submit article"
		payload ["timestamp"] = get_timestamp()
		return Response(payload)

	def put(self, request, postID=None):
		try:
			payload = dict()
			check_passed = check_admin_api(request.user)

			postID = int(postID)

			if type(postID) is not int or postID < 1:
				raise Exception("postID parameter is not valid")

			if check_passed != True:
				raise Exception(check_passed)
			else:
				feedname = request.user.username
				payload ["username"] = request.user.username

			title = unicodedata.normalize('NFC', request.data['title'])
			link = unicodedata.normalize('NFC', request.data['link'])

			if title == "" or link == "":
				raise Exception("Title and/or Link is/are missing")

			tags = unicodedata.normalize('NFC', request.data['tags']).split(',') # We separate each tag and create a list out of it.

			activated_bool = str2bool(unicodedata.normalize('NFC', request.data['activated']))
			twitter_bool = str2bool(unicodedata.normalize('NFC', request.data['twitter']))

			if str2bool(unicodedata.normalize('NFC', request.data['autoformat'])) :
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
		return Response(payload)

	def delete(self, request, postID=None):
		try:
			payload = dict()
			check_passed = check_admin_api(request.user)

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
		return Response(payload)

class Modify_Social_Networks(APIView):

	def put(self, request):
		try:
			payload = dict()
			check_passed = check_admin_api(request.user)

			if check_passed != True:
				raise Exception(check_passed)

			feedname = request.user.username
			payload ["username"] = request.user.username

			val = URLValidator()

			social_networks = [
				'dribbble',
				'facebook',
				'flickr',
				'gplus',
				'instagram',
				'linkedin',
				'pinterest',
				'stumble',
				'twitter',
				'vimeo',
				'youtube',
				'docker',
				'git',
				'kaggle',
				'coursera',
				'googlescholar',
				'orcid',
				'researchgate',
				'blog',
				'website'
			]

			social_data = {}
			for social in social_networks:
				url = unicodedata.normalize('NFC', request.data[social])
				if url != '':
					try:
						val(url) #Raise a ValidationError if the URL is invalid.
					except:
						raise Exception("URL Not Valid: "+social)
				social_data[social] = url

			tmp_user = FeedUser.objects.get(username=request.user.username)

			# Main Social Networks
			tmp_user.social_dribbble = social_data['dribbble']
			tmp_user.social_facebook = social_data['facebook']
			tmp_user.social_flickr = social_data['flickr']
			tmp_user.social_gplus = social_data['gplus']
			tmp_user.social_instagram = social_data['instagram']
			tmp_user.social_linkedin = social_data['linkedin']
			tmp_user.social_pinterest = social_data['pinterest']
			tmp_user.social_stumble = social_data['stumble']
			tmp_user.social_twitter = social_data['twitter']
			tmp_user.social_vimeo = social_data['vimeo']
			tmp_user.social_youtube = social_data['youtube']

			# Computer Science Networks
			tmp_user.social_docker = social_data['docker']
			tmp_user.social_git = social_data['git']
			tmp_user.social_kaggle = social_data['kaggle']

			# MooC Profiles
			tmp_user.social_coursera = social_data['coursera']

			# Research Social Networks
			tmp_user.social_google_scholar = social_data['googlescholar']
			tmp_user.social_orcid = social_data['orcid']
			tmp_user.social_researchgate = social_data['researchgate']
			tmp_user.social_blog = social_data['blog']
			tmp_user.social_personalwebsite = social_data['website']

			tmp_user.save()
			payload["success"] = True

		except Exception, e:
			payload["success"] = False
			payload["error"] = "An error occured in the process: " + str(e)
			payload["postID"] = None


		payload ["operation"] = "modify social networks"
		payload ["timestamp"] = get_timestamp()
		return Response(payload)

class Modify_Personal_info(APIView):
	def put(self, request):
		try:
			payload = dict()
			check_passed = check_admin_api(request.user)

			if check_passed != True:
				raise Exception(check_passed)

			feedname = request.user.username
			payload ["username"] = request.user.username

			val = URLValidator()

			fields = [
				'firstname',
				'lastname',
				'email',
				'birthdate',
				'country',
				'gender',
				'feedtitle', # not Checked
				'description', # not Checked
				'job', # not Checked
				'company_name', # not Checked
				'company_website',
				"newsletter_subscribtion", # Not Saved yet !
			]

			profile_data = {}
			for field in fields:
				profile_data[field] = unicodedata.normalize('NFC', request.POST[field])

			FeedUser.objects._validate_firstname(profile_data["firstname"])
			FeedUser.objects._validate_lastname(profile_data["lastname"])
			FeedUser.objects._validate_email(profile_data["email"])
			FeedUser.objects._validate_birthdate(profile_data["birthdate"])

			FeedUser.objects._validate_country(profile_data["country"])
			FeedUser.objects._validate_gender(profile_data["gender"])

			val(profile_data["company_website"])

			request.user.first_name = profile_data["firstname"]
			request.user.last_name = profile_data["lastname"]
			request.user.email = profile_data["email"]
			request.user.birthdate = datetime.datetime.strptime(profile_data["birthdate"], '%d/%m/%Y').date()
			request.user.country = Country.objects.get(name=profile_data["country"])
			request.user.gender = profile_data["gender"]
			request.user.rss_feed_title = profile_data["feedtitle"]
			request.user.description = profile_data["description"]
			request.user.job = profile_data["job"]
			request.user.company_name = profile_data["company_name"]
			request.user.company_website = profile_data["company_website"]

			request.user.save()
			payload["success"] = True

		except Exception, e:
			payload["success"] = False
			payload["error"] = "An error occured in the process: " + str(e)
			payload["postID"] = None

		payload ["operation"] = "modify personal Information"
		payload ["timestamp"] = get_timestamp()
		return Response(payload)

class Modify_Password(APIView):
	def put(self, request):
		try:
			payload = dict()
			check_passed = check_admin_api(request.user)

			if check_passed != True:
				raise Exception(check_passed)

			feedname = request.user.username
			payload ["username"] = request.user.username


			payload["success"] = True

		except Exception, e:
			payload["success"] = False
			payload["error"] = "An error occured in the process: " + str(e)
			payload["postID"] = None

		payload ["operation"] = "modify personal Information"
		payload ["timestamp"] = get_timestamp()
		return Response(payload)

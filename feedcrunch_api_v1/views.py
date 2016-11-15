#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser

from django_q.tasks import async, schedule
from django_q.models import Schedule

from feedcrunch.models import Post, FeedUser, Tag, Country, RSSFeed

from twitter.tw_funcs import TwitterAPI, get_authorization_url

import datetime, unicodedata, json, sys, os, feedparser

from check_admin import check_admin_api
from time_funcs import get_timestamp
from date_manipulation import get_N_time_period
from data_convert import str2bool
from ap_style import format_title
from image_validation import get_image_dimensions
from feed_validation import validate_feed
from clean_html import clean_html

class Username_Validation(APIView):

	def post(self, request):

		try:

			payload = dict()
			username = request.POST.get('username')
			payload ["username"] = username

			if username == None:
				raise Exception("Username not provided")

			else:
				username = username.lower() # Make it Lowercase
				payload ["available"] = not FeedUser.objects.filter(username = username).exists()
				payload ["success"] = True

		except Exception, e:
			payload["success"] = False
			payload["error"] = "An error occured in the process: " + str(e)

		payload["operation"] = "Username Validation"
		payload ["timestamp"] = get_timestamp()
		return Response(payload)

class rssfeed_Validation(APIView):

	def post(self, request):

		try:

			payload = dict()
			rssfeed = request.POST.get('rssfeed')
			payload ["rssfeed"] = rssfeed

			if rssfeed == None:
				raise Exception("Link for the RSS Feed not provided")

			else:

				if RSSFeed.objects.filter(link=rssfeed, user=request.user).exists():
					payload ["valid"] = False
					payload ["error"] = "You already subscribed to this RSS Feed"

				else:
					rss_data = feedparser.parse(rssfeed)

					if validate_feed(rss_data):
						payload ["valid"] = True
						payload ["title"] = clean_html(rss_data.feed.title)

					else:
						payload ["valid"] = False
						payload ["error"] = "The RSS Feed is not valid. Please check your link"

				payload ["success"] = True

		except Exception, e:
			payload["success"] = False
			payload["error"] = "An error occured in the process: " + str(e)

		payload["operation"] = "RSS Feed Validation"
		payload ["timestamp"] = get_timestamp()
		return Response(payload)

class User_Stats_Subscribers(APIView):

	def get(self, request):
		try:

			payload = dict()
			check_passed = check_admin_api(request.user)

			if check_passed != True:
				raise Exception(check_passed)

			payload ["success"] = True
			payload ["username"] = request.user.username

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

			payload ["success"] = True
			payload ["username"] = request.user.username

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

class RSSFeed_View(APIView): # Add Article (POST), Get Article  (GET), Modify Article  (PUT), DELETE Article (DELETE)

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

				title = unicodedata.normalize('NFC', request.POST['rssfeed_title'])
				link = unicodedata.normalize('NFC', request.POST['rssfeed_link'])

				tmp_rssfeed = RSSFeed.objects.create(title=title, link=link, user=request.user)

				schedule('feedcrunch.tasks.check_rss_feed', rss_id=tmp_rssfeed.id, schedule_type=Schedule.ONCE, next_run=timezone.now() + datetime.timedelta(minutes=1))

				payload["success"] = True
				payload["RSSFeedID"] = str(tmp_rssfeed.id)

		except Exception, e:
			payload["success"] = False
			payload["error"] = "An error occured in the process: " + str(e)

		payload["operation"] = "subscribe to RSS Feed"
		payload ["timestamp"] = get_timestamp()
		return Response(payload)

	def put(self, request, feedID=None):
		try:
			payload = dict()
			check_passed = check_admin_api(request.user)

			feedID = int(unicodedata.normalize('NFC', feedID))

			if type(feedID) is not int or feedID < 1:
				raise Exception("feedID parameter is not valid")

			if check_passed != True:
				raise Exception(check_passed)

			payload ["username"] = request.user.username

			query_set = RSSFeed.objects.filter(id=feedID, user=request.user)

			if query_set.count() == 0:
				raise Exception("Feed ID = "+ feedID +" does not exist for the user: " + payload ["username"])

			feed = query_set[0]

			title = unicodedata.normalize('NFC', request.POST['rssfeed_title'])
			link = unicodedata.normalize('NFC', request.POST['rssfeed_link'])

			if title == "" or link == "":
				raise Exception("Title and/or Link is/are missing")

			feed.title = title
			feed.link = link

			feed.save()

			schedule('feedcrunch.tasks.check_rss_feed', rss_id=feed.id, schedule_type=Schedule.ONCE, next_run=timezone.now() + datetime.timedelta(minutes=1))

			payload["success"] = True
			payload["feedID"] = str(feedID)

		except Exception, e:
			payload["success"] = False
			payload["error"] = "An error occured in the process: " + str(e)
			payload["postID"] = None


		payload["operation"] = "modify RSSFeed"
		payload ["timestamp"] = get_timestamp()
		return Response(payload)

	def delete(self, request, feedID=None):
		try:
			payload = dict()
			check_passed = check_admin_api(request.user)

			feedID = int(unicodedata.normalize('NFC', feedID))

			if type(feedID) is not int or feedID < 1:
				raise Exception("feedID parameter is not valid")

			if check_passed != True:
				raise Exception(check_passed)

			payload ["username"] = request.user.username

			query_set = RSSFeed.objects.filter(id=feedID, user=payload ["username"])

			if query_set.count() == 0:
				raise Exception("Feed ID = "+ feedID +" does not exist for the user: " + payload ["username"])

			query_set[0].delete()

			payload ["success"] = True
			payload["postID"] = feedID

		except Exception, e:
			payload["success"] = False
			payload["error"] = "An error occured in the process: " + str(e)
			payload["postID"] = None

		payload ["operation"] = "delete RSS Feed"
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

			tmp_post = Post.objects.create(title=title, link=link, clicks=0, user=request.user, activeLink=activated_bool)

			for tag in tags:
				tmp_obj, created_bool = Tag.objects.get_or_create(name=tag)
				tmp_post.tags.add(tmp_obj)

			tmp_post.save()

			if twitter_bool and request.user.is_twitter_enabled():

					twitter_instance = TwitterAPI(request.user)

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

			tmp_post = Post.objects.get(id=postID, user=request.user)

			tmp_post.title = title
			tmp_post.link = link
			tmp_post.activeLink = activated_bool
			tmp_post.tags.clear()

			for tag in tags:
				tmp_obj, created_bool = Tag.objects.get_or_create(name=tag)
				tmp_post.tags.add(tmp_obj)

			if twitter_bool and request.user.is_twitter_enabled():

				twitter_instance = TwitterAPI(request.user)

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

			payload ["username"] = request.user.username

			post = Post.objects.filter(id=postID, user=request.user)
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

			# Main Social Networks
			request.user.social_dribbble = social_data['dribbble']
			request.user.social_facebook = social_data['facebook']
			request.user.social_flickr = social_data['flickr']
			request.user.social_gplus = social_data['gplus']
			request.user.social_instagram = social_data['instagram']
			request.user.social_linkedin = social_data['linkedin']
			request.user.social_pinterest = social_data['pinterest']
			request.user.social_stumble = social_data['stumble']
			request.user.social_twitter = social_data['twitter']
			request.user.social_vimeo = social_data['vimeo']
			request.user.social_youtube = social_data['youtube']

			# Computer Science Networks
			request.user.social_docker = social_data['docker']
			request.user.social_git = social_data['git']
			request.user.social_kaggle = social_data['kaggle']

			# MooC Profiles
			request.user.social_coursera = social_data['coursera']

			# Research Social Networks
			request.user.social_google_scholar = social_data['googlescholar']
			request.user.social_orcid = social_data['orcid']
			request.user.social_researchgate = social_data['researchgate']
			request.user.social_blog = social_data['blog']
			request.user.social_personalwebsite = social_data['website']

			request.user.save()
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

			form_data = {}
			for field in fields:
				form_data[field] = unicodedata.normalize('NFC', request.data[field])

			FeedUser.objects._validate_firstname(form_data["firstname"])
			FeedUser.objects._validate_lastname(form_data["lastname"])
			FeedUser.objects._validate_email(form_data["email"])
			FeedUser.objects._validate_birthdate(form_data["birthdate"])

			FeedUser.objects._validate_country(form_data["country"])
			FeedUser.objects._validate_gender(form_data["gender"])

			val(form_data["company_website"])

			request.user.first_name = form_data["firstname"]
			request.user.last_name = form_data["lastname"]
			request.user.email = form_data["email"]
			request.user.birthdate = datetime.datetime.strptime(form_data["birthdate"], '%d/%m/%Y').date()
			request.user.country = Country.objects.get(name=form_data["country"])
			request.user.gender = form_data["gender"]
			request.user.rss_feed_title = form_data["feedtitle"]
			request.user.description = form_data["description"]
			request.user.job = form_data["job"]
			request.user.company_name = form_data["company_name"]
			request.user.company_website = form_data["company_website"]

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

			payload ["username"] = request.user.username

			form_fields = [
				'old_password',
				'new_password_1',
				'new_password_2',
			]

			form_data = {}

			for field in form_fields:
				form_data[field] = unicodedata.normalize('NFC', request.data[field])

			if (not request.user.check_password(form_data['old_password'])):
				raise Exception("Old Password is incorrect")

			if ( form_data['new_password_1'] != form_data['new_password_2'] ):
				raise Exception("Your have input two different passwords, please retry.")

			request.user.set_password(form_data['new_password_1'])

			payload["success"] = True

		except Exception, e:
			payload["success"] = False
			payload["error"] = "An error occured in the process: " + str(e)
			payload["postID"] = None

		payload ["operation"] = "modify password"
		payload ["timestamp"] = get_timestamp()
		return Response(payload)

'''
class Modify_Photo(APIView):
	parser_classes = (FileUploadParser,)

	def put(self, request, filename=""):
		try:
			payload = dict()
			check_passed = check_admin_api(request.user)

			if check_passed != True:
				raise Exception(check_passed)
			payload ["username"] = request.user.username

			#unicodedata.normalize('NFC', request.data["photo"])
			photo = request.data['photo']

			allowed_mime_types = ['image/gif', 'image/jpeg', 'image/pjpeg', 'image/png']

			if photo.content_type not in allowed_mime_types:
				raise ValueError("Only Images are allowed.")

			w, h = get_image_dimensions(photo.read())

			if isinstance(w, int) and isinstance(h, int) and w > 0 and h > 0 :

				if photo.size > 1000000: # > 1MB
					raise ValueError("File size is larger than 1MB.")

				request.user = FeedUser.objects.get(username=request.user.username)
				request.user.profile_picture = photo
				request.user.save()
			else:
				raise ValueError("The uploaded image is not valid")

			payload["success"] = True

		except Exception, e:
			payload["success"] = False
			payload["error"] = "An error occured in the process: " + str(e)
			payload["postID"] = None

		payload ["operation"] = "modify profile picture"
		payload ["timestamp"] = get_timestamp()
		return Response(payload)
'''

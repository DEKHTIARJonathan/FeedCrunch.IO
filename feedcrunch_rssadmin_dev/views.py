#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

import datetime, unicodedata, json
from calendar import monthrange

from feedcrunch.models import Post, FeedUser, Country, Tag
from twitter.tw_funcs import TwitterAPI, get_authorization_url

from check_admin import check_admin
from data_convert import str2bool
from ap_style import format_title
from image_validation import get_image_dimensions
from custom_render import myrender as render

# Create your views here.

def index(request, feedname=None):

	check_passed = check_admin(feedname, request.user)
	if check_passed != True:
		return check_passed
	else:
		if not request.user.is_twitter_activated():
			auth_url = get_authorization_url(request)
		else:
			auth_url = False # False => Don't need to authenticate with Twitter

		country_list = Country.objects.all().order_by('name')

		d = datetime.datetime.now()
		monthtime_elapsed = int(round(float(d.day) / monthrange(d.year, d.month)[1] * 100,0))

		try:
			publication_trend = ((float(request.user.get_current_month_post_count()) / request.user.get_last_month_post_count()) -1 ) * 100.0

			if publication_trend > 0:
				post_trending = "trending_up"
				post_trending_color = "green-text"
			elif publication_trend < 0:
				post_trending = "trending_down"
				post_trending_color = "red-text"
			else :
				post_trending = "trending_flat"
				post_trending_color = "blue-grey lighten-1"

			publication_trend = int(round(abs(publication_trend),0))

		except ZeroDivisionError:
			publication_trend = -1
			post_trending = "new_releases"

		data = {
			'auth_url': auth_url,
			'countries': country_list,
			'monthtime_elapsed': monthtime_elapsed,
			'post_trending': post_trending,
			'publication_trend': publication_trend,
			'post_trending_color': post_trending_color,
		}

		return render(request, 'admin_dev/admin_index.html', data)

'''
def add_form(request, feedname=None):

	check_passed = check_admin(feedname, request.user)
	if check_passed != True:
		return check_passed
	else:
		return render(request, 'post_form.html', {})

def update_info(request, feedname=None):

	data = {}
	data["operation"] = "update_info"

	val = URLValidator()

	if request.method == 'POST':

		if check_admin(feedname, request.user) != True:
			data["status"] = "error"
			data["error"] = "You are not allowed to perform this action"
			data["feedname"] = str(feedname)
		else:
			try:
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
					'company_website'
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

				tmp_user = FeedUser.objects.get(username=request.user.username)

				tmp_user.first_name = profile_data["firstname"]
				tmp_user.last_name = profile_data["lastname"]
				tmp_user.email = profile_data["email"]
				tmp_user.birthdate = datetime.datetime.strptime(profile_data["birthdate"], '%d/%m/%Y').date()
				tmp_user.country = Country.objects.get(name=profile_data["country"])
				tmp_user.gender = profile_data["gender"]
				tmp_user.rss_feed_title = profile_data["feedtitle"]
				tmp_user.description = profile_data["description"]
				tmp_user.job = profile_data["job"]
				tmp_user.company_name = profile_data["company_name"]
				tmp_user.company_website = profile_data["company_website"]

				tmp_user.save()

				return HttpResponseRedirect('/@'+request.user.username+'/admin')

			except Exception, e:
				data["status"] = "error"
				data["error"] = "An error occured in the process: " + str(e)
				data["feedname"] = feedname

	else:
		data["status"] = "error"
		data["error"] = "Only available with a POST Request"
		data["feedname"] = feedname

	return JsonResponse(data)

def tags_ajax_json(request, feedname=None):
	data = {}
	data["operation"] = "get_tags"

	if request.method == 'GET':

		if check_admin(feedname, request.user) != True:
			data["status"] = "error"
			data["error"] = "You are not allowed to perform this action"
			data["feedname"] = str(feedname)

		else:
			tags = Tag.objects.all().order_by('name')
			data["tags"] = [tag.name for tag in tags]

	else:
		data["status"] = "error"
		data["error"] = "Only available with a GET Request"
		data["feedname"] = feedname

	return JsonResponse(data, safe=False)

def update_password(request, feedname=None):

	data = {}
	data["operation"] = "update_password"

	if request.method == 'POST':

		if check_admin(feedname, request.user) != True:
			data["status"] = "error"
			data["error"] = "You are not allowed to perform this action"
			data["feedname"] = str(feedname)
		else:
			try:
				password1 = unicodedata.normalize('NFC', request.POST["password1"])
				password2 = unicodedata.normalize('NFC', request.POST["password2"])

				if password1 != password2:
					raise ValueError("The given passwords are different.")
				else:

					tmp_user = FeedUser.objects.get(username=request.user.username)

					FeedUser.objects._validate_password(password1)

					tmp_user.set_password(password1)
					tmp_user.save()

					return HttpResponseRedirect('/@'+request.user.username+'/admin')

			except Exception, e:
				data["status"] = "error"
				data["error"] = "An error occured in the process: " + str(e)
				data["feedname"] = feedname

	else:
		data["status"] = "error"
		data["error"] = "Only available with a POST Request"
		data["feedname"] = feedname

	return JsonResponse(data)

def update_photo(request, feedname=None):

	data = {}
	data["operation"] = "update_photo"

	if request.method == 'POST':

		if check_admin(feedname, request.user) != True:
			data["status"] = "error"
			data["error"] = "You are not allowed to perform this action"
			data["feedname"] = str(feedname)
		else:
			try:
				photo = request.FILES['photo']

				allowed_mime_types = ['image/gif', 'image/jpeg', 'image/pjpeg', 'image/png']

				if photo.content_type not in allowed_mime_types:
					raise ValueError("Only Images are allowed.")

				w, h = get_image_dimensions(photo.read())

				if isinstance(w, int) and isinstance(h, int) and w > 0 and h > 0 :

					if photo.size > 1000000: # > 1MB
						raise ValueError("File size is larger than 1MB.")

					tmp_user = FeedUser.objects.get(username=request.user.username)
					tmp_user.profile_picture = photo
					tmp_user.save()
				else:
					raise ValueError("The uploaded image is not valid")

				return HttpResponseRedirect('/@'+request.user.username+'/admin')

			except Exception, e:
				data["status"] = "error"
				data["error"] = "An error occured in the process: " + str(e)
				data["feedname"] = feedname

	else:
		data["status"] = "error"
		data["error"] = "Only available with a POST Request"
		data["feedname"] = feedname

	return JsonResponse(data)

def update_social_links(request, feedname=None):

	val = URLValidator()

	data = {}
	data["operation"] = "update_social_links"

	if request.method == 'POST':

		if check_admin(feedname, request.user) != True:
			data["status"] = "error"
			data["error"] = "You are not allowed to perform this action"
			data["feedname"] = str(feedname)
		else:
			try:
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
					url = unicodedata.normalize('NFC', request.POST[social])
					if url != '':
						val(url) #Raise a ValidationError if the URL is invalid.
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
				return HttpResponseRedirect('/@'+request.user.username+'/admin')

			except Exception, e:
				data["status"] = "error"
				data["error"] = "An error occured in the process: " + str(e)
				data["feedname"] = feedname

	else:
		data["status"] = "error"
		data["error"] = "Only available with a POST Request"
		data["feedname"] = feedname

	return JsonResponse(data)

def add_form_ajax(request, feedname=None):

	data = {}
	data["operation"] = "insert"

	if request.method == 'POST':

		if check_admin(feedname, request.user) != True:
			data["status"] = "error"
			data["error"] = "You are not allowed to perform this action"
		else:
			try:
				title = unicodedata.normalize('NFC', request.POST['title'])
				link = unicodedata.normalize('NFC', request.POST['link'])
				tags = unicodedata.normalize('NFC', request.POST['tags']).split() # We separate each tag and create a list out of it.

				activated_bool = str2bool(unicodedata.normalize('NFC', request.POST['activated']))
				twitter_bool = str2bool(unicodedata.normalize('NFC', request.POST['twitter']))

				if str2bool(unicodedata.normalize('NFC', request.POST['autoformat'])) :
					title = format_title(title)

				if title == "" or link == "":
					data["status"] = "error"
					data["error"] = "Title and/or Link is/are missing"

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
									data["status"] = "error"
									data["postID"] = str(tmp_post.id)
									data["error"] = "An error occured in the twitter posting process, but the post was saved: " + tw_rslt['error']

								else:
									data["status"] = "success"
									data["postID"] = str(tmp_post.id)

							else:
								raise Exception("Not connected to the Twitter API")

					else:
						tmp_post.save()
						data["status"] = "success"
						data["postID"] = str(tmp_post.id)

			except Exception, e:
				data["status"] = "error"
				data["error"] = "An error occured in the process: " + str(e)
				data["postID"] = None

	else:
		data["status"] = "error"
		data["error"] = "Only available with a POST Request"

	return JsonResponse(data)

def modify_form_ajax(request, feedname=None, postID=None):

	data = {}
	data["operation"] = "modification"

	if request.method == 'POST':

		if check_admin(feedname, request.user) != True:
			data["status"] = "error"
			data["error"] = "You are not allowed to perform this action"
			data["postID"] = str(postID)

		elif postID == None:
			data["status"] = "error"
			data["error"] = "postID parameter is missing"
			data["postID"] = ""

		else:
			try:
				title = unicodedata.normalize('NFC', request.POST['title'])
				link = unicodedata.normalize('NFC', request.POST['link'])
				tags = unicodedata.normalize('NFC', request.POST['tags']).split() # We separate each tag and create a list out of it.

				activated_bool = str2bool(unicodedata.normalize('NFC', request.POST['activated']))
				twitter_bool = str2bool(unicodedata.normalize('NFC', request.POST['twitter']))

				if str2bool(unicodedata.normalize('NFC', request.POST['autoformat'])) :
					title = format_title(title)

				if title == "" or link == "":
					raise Exception("Data Missing")

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
								data["status"] = "error"
								data["postID"] = str(tmp_post.id)
								data["error"] = "An error occured in the twitter posting process, but the post was saved: " + tw_rslt['error']

							else:
								data["status"] = "success"
								data["postID"] = str(tmp_post.id)

						else:
							raise Exception("Not connected to the Twitter API")

				else:
					tmp_post.save()
					data["status"] = "success"
					data["postID"] = str(postID)


			except Exception, e:
				data["status"] = "error"
				data["error"] = str(e)
				data["postID"] = str(postID)

	else:
		data["status"] = "error"
		data["error"] = "Only available with a POST Request"
		data["postID"] = str(postID)

	return JsonResponse(data)

def modify_listing(request, feedname=None):

	check_passed = check_admin(feedname, request.user)
	if check_passed != True:
		return check_passed
	else:
		posts = Post.objects.filter(user = feedname).order_by('-id')
		return render(request, 'listing.html', {'posts': posts})

def modify_form(request, feedname=None, postID=None):

	check_passed = check_admin(feedname, request.user)
	if check_passed != True:
		return check_passed

	elif postID == None:
		return HttpResponseRedirect("/@"+feedname+"/admin/modify")

	else:
		try:
			post = Post.objects.get(id=postID, user=feedname)
			return render(request, 'post_form.html', {"post": post})

		except:
			return HttpResponseRedirect("/@"+feedname+"/admin/modify")

def delete_ajax(request, feedname=None):

	data = {}
	data["operation"] = "delete"

	if request.method == 'POST':

		if check_admin(feedname, request.user) != True:
			data["status"] = "error"
			data["error"] = "You are not allowed to perform this action"
			data["postID"] = str(postID)
		else:
			try:
				postID = int(unicodedata.normalize('NFC', request.POST['postID']))

				if type(postID) is not int or postID < 1:
					data["status"] = "error"
					data["error"] = "postID parameter is not valid"
					data["postID"] = str(postID)

				else:

					Post.objects.filter(id=postID, user=feedname).delete()
					data["status"] = "success"
					data["postID"] = str(postID)

			except:
				data["status"] = "error"
				data["error"] = "An error occured in the process"
				data["postID"] = str(postID)


	else:
		data["status"] = "error"
		data["error"] = "Only available with a POST Request"
		data["postID"] = str(postID)

	return JsonResponse(data)

def delete_listing(request, feedname=None):

	check_passed = check_admin(feedname, request.user)
	if check_passed != True:
		return check_passed
	else:
		posts = Post.objects.filter(user = feedname).order_by('-id')
		return render(request, 'listing.html', {'posts': posts})

'''

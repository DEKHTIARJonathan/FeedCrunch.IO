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

from feedcrunch.models import Post, FeedUser, Country, Tag, RSSFeed, RSSArticle, RSSFeed_Sub, RSSArticle_Assoc
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
			post_trending_color = "blue-grey lighten-1"

		data = {
			'auth_url': auth_url,
			'countries': country_list,
			'monthtime_elapsed': monthtime_elapsed,
			'post_trending': post_trending,
			'publication_trend': publication_trend,
			'post_trending_color': post_trending_color,
		}

		return render(request, 'admin/admin_dashboard.html', data)

def personal_info_form(request, feedname=None):

	check_passed = check_admin(feedname, request.user)
	if check_passed != True:
		return check_passed

	else:

		country_list = Country.objects.all().order_by('name')
		return render(request, 'admin/admin_personal.html', {'countries': country_list})

def preferences_form(request, feedname=None):

	check_passed = check_admin(feedname, request.user)
	if check_passed != True:
		return check_passed
	else:
		return render(request, 'admin/admin_preferences.html')

def password_form(request, feedname=None):

	check_passed = check_admin(feedname, request.user)
	if check_passed != True:
		return check_passed
	else:
		return render(request, 'admin/admin_password.html')

def picture_form(request, feedname=None):

	check_passed = check_admin(feedname, request.user)
	if check_passed != True:
		return check_passed
	else:
		return render(request, 'admin/admin_photo.html')

def social_form(request, feedname=None):

	check_passed = check_admin(feedname, request.user)
	if check_passed != True:
		return check_passed
	else:
		return render(request, 'admin/admin_social_accounts.html')

def services_form(request, feedname=None):

	check_passed = check_admin(feedname, request.user)
	if check_passed != True:
		return check_passed
	else:
		if not request.user.is_twitter_activated():
			twitter_auth_url = get_authorization_url(request)
		else:
			twitter_auth_url = False # False => Don't need to authenticate with Twitter
		return render(request, 'admin/admin_social_sharing.html', {'twitter_auth_url': twitter_auth_url})

def add_article_form(request, feedname=None):

	check_passed = check_admin(feedname, request.user)
	if check_passed != True:
		return check_passed
	else:
		return render(request, 'admin/admin_article_form.html')

def modify_article_form(request, feedname=None, postID=None):

	check_passed = check_admin(feedname, request.user)
	if check_passed != True:
		return check_passed

	elif postID == None:
		return HttpResponseRedirect("/@"+feedname+"/admin/modify")

	else:
		try:
			post = Post.objects.get(id=postID, user=feedname)
			print request.user.is_twitter_enabled()
			return render(request, 'admin/admin_article_form.html', {"post": post})

		except:
			return HttpResponseRedirect("/@"+feedname+"/admin/modify")

def modify_article_listing(request, feedname=None):

	check_passed = check_admin(feedname, request.user)
	if check_passed != True:
		return check_passed
	else:
		posts = Post.objects.filter(user = feedname).order_by('-id')
		return render(request, 'admin/admin_post_listing.html', {'posts': posts})

def delete_article_listing(request, feedname=None):

	check_passed = check_admin(feedname, request.user)
	if check_passed != True:
		return check_passed
	else:
		posts = Post.objects.filter(user = feedname).order_by('-id')
		return render(request, 'admin/admin_post_listing.html', {'posts': posts})

def contact_form(request, feedname=None):

	check_passed = check_admin(feedname, request.user)
	if check_passed != True:
		return check_passed
	else:
		return render(request, 'admin/admin_contact.html')

def upload_picture(request, feedname=None):
	try:

		if request.method == 'POST':

			if check_admin(feedname, request.user) != True:
				raise Exception("You are not allowed to perform this action")

			else:
				photo = request.FILES['photo']

				allowed_mime_types = ['image/gif', 'image/jpeg', 'image/pjpeg', 'image/png']

				if photo.content_type not in allowed_mime_types:
					raise ValueError("Only Images are allowed.")


				"""
				# Not functioning at the time
				w, h = get_image_dimensions(photo.read())
				if not(isinstance(w, int) and isinstance(h, int) and w > 0 and h > 0):
					raise ValueError("Picture dimensions are not correct.")

				"""
				if photo.size > 1048576: # > 1MB
					raise ValueError("File size is larger than 1MB.")

				else:
					tmp_user = FeedUser.objects.get(username=request.user.username)
					tmp_user.profile_picture = photo
					tmp_user.save()

		else:
			raise Exception("Only POST Requests Allowed.")

	except Exception, e:
		data = {}
		data["status"] = "error"
		data["error"] = "An error occured in the process: " + str(e)
		data["feedname"] = feedname
		return JsonResponse(data)

	return HttpResponseRedirect('/@'+request.user.username+'/admin/account/picture/')

def sub_management(request, feedname=None):
	check_passed = check_admin(feedname, request.user)
	if check_passed != True:
		return check_passed
	else:
		feeds = RSSFeed_Sub.objects.filter(user=feedname, feed__active=True).order_by("title")
		return render(request, 'admin/admin_sub_listing.html', {'feeds': feeds})

def reading_recommendation(request, feedname=None):
	check_passed = check_admin(feedname, request.user)
	if check_passed != True:
		return check_passed
	else:
		#rssarticles = RSSArticle_Assoc.objects.filter(rel_sub_article_assoc__user=request.user, rel_sub_article_assoc__marked_read = False).order_by('-added_date')
		rssarticles = RSSArticle_Assoc.objects.filter(user=request.user, marked_read = False).order_by('-article__added_date')

		rssarticles_data = []

		max_size = len(rssarticles)

		if max_size > 30:
			max_size = 30

		for i in range(max_size):
			recommendation_score = 97.3 - 1.2*i
			tmp = {
				'id': rssarticles[i].id,
				'short_title': rssarticles[i].short_title(),
				'title': rssarticles[i].title(),
				'rssfeed': rssarticles[i].short_rssfeed(),
				'get_domain': rssarticles[i].short_domain(),
				'link': rssarticles[i].link(),
				'score': recommendation_score,
				'color': int(2.55*recommendation_score),
				'get_shortdate': rssarticles[i].get_shortdate(),
			}
			rssarticles_data.append(tmp)

		return render(request, 'admin/admin_reading_recommendation.html', {'rssarticles': rssarticles_data})

def redirect_recommendation(request, feedname=None, RSSArticle_AssocID=None):
	check_passed = check_admin(feedname, request.user)
	if check_passed != True:
		return check_passed

	try:
		tmp_article = RSSArticle_Assoc.objects.get(id=RSSArticle_AssocID, user=feedname)

		tmp_article.open_count += 1
		tmp_article.save()

		return HttpResponseRedirect(tmp_article.article.link)
	except:
		return HttpResponseRedirect("/@"+feedname+"/admin/reading/recommendation/")

def onboarding_interests(request, feedname=None):

	check_passed = check_admin(feedname, request.user)
	if check_passed != True:
		return check_passed

	else:
		return render(request, 'onboarding/interests.html')

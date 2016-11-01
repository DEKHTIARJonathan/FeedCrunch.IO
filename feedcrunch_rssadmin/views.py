#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext, loader

import datetime, unicodedata, json, sys, os
from calendar import monthrange

from feedcrunch.models import Post, FeedUser, Country, Tag
from twitter.tw_funcs import TwitterAPI, get_authorization_url

from custom_render import myrender as render
from check_admin import check_admin
from data_convert import str2bool
from ap_style import format_title
from image_validation import get_image_dimensions

# Create your views here.

def dummy(request, feedname=None, postID=None):
	return HttpResponse("Dummy")

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

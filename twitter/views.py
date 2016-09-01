#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from feedcrunch.models import FeedUser, Option

import feedcrunch_rssadmin.views as adminviews

from .tw_funcs import *
from twython import Twython

def get_callback(request):

	try:

		oauth_verifier = request.GET['oauth_verifier']

		token = request.session['OAUTH_TOKEN']

		token_secret = request.session['OAUTH_TOKEN_SECRET']

		tw_request = get_authorized_tokens(oauth_verifier, token, token_secret)

		if not tw_request['status']:
			raise Exception(request['error'])

		usr_tmp = FeedUser.objects.get(username=request.user.username)

		usr_tmp.twitter_token = tw_request['tokens']['oauth_token']
		usr_tmp.twitter_token_secret = tw_request['tokens']['oauth_token_secret']

		usr_tmp.save()

		return HttpResponseRedirect(reverse(adminviews.index, kwargs={'feedname': request.user.username}))

	except Exception, e:
		data = {}

		data["status"] = "error"
		data["error"] = str(e)
		data["feedname"] = request.user.username

		return JsonResponse(data)

def unlink(request):
	usr_tmp = FeedUser.objects.get(username=request.user.username)
	usr_tmp.reset_twitter_credentials()

	return HttpResponseRedirect(reverse(adminviews.index, kwargs={'feedname': request.user.username}))

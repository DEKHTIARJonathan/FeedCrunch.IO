#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse

from datetime import datetime, timedelta

from oauth.twitterAPI  import TwitterAPI
from oauth.facebookAPI import FacebookAPI
from oauth.linkedinAPI import LinkedInAPI
from oauth.slackAPI    import SlackAPI

from feedcrunch.models import SlackIntegration

def twitter_callback(request):

    try:

        oauth_verifier = request.GET['oauth_verifier']
        token          = request.session['OAUTH_TOKEN']
        token_secret   = request.session['OAUTH_TOKEN_SECRET']

        tw_request = TwitterAPI.get_authorized_tokens(oauth_verifier, token, token_secret)

        if not tw_request['status']:
            raise Exception(tw_request['error'])

        setattr(request.user, request.user.social_fields["twitter"]["token"], tw_request['oauth_token'])
        setattr(request.user, request.user.social_fields["twitter"]["secret"], tw_request['oauth_token_secret'])

        request.user.save()

        return render(request, 'admin/self_closing.html')

    except Exception as e:
        data = dict()

        data["status"] = "error"
        data["error"] = str(e)
        data["feedname"] = request.user.username

        return JsonResponse(data)

def facebook_callback(request):

    try:
        access_code = request.GET['code']

        fb_request = FacebookAPI.get_authorized_tokens(access_code)

        if not fb_request['status']:
            raise Exception(fb_request['error'])

        expire_datetime = datetime.now() + timedelta(seconds=int(fb_request['expires_in']))

        setattr(request.user, request.user.social_fields["facebook"]["token"], fb_request['access_token'])
        setattr(request.user, request.user.social_fields["facebook"]["expire_datetime"], expire_datetime)

        request.user.save()

        return render(request, 'admin/self_closing.html')

    except Exception as e:
        data = dict()

        data["status"] = "error"
        data["error"] = str(e)
        data["feedname"] = request.user.username

        return JsonResponse(data)

def linkedin_callback(request):

    try:
        access_code = request.GET['code']

        lk_request = LinkedInAPI.get_authorized_tokens(access_code)

        if not lk_request['status']:
            raise Exception(lk_request['error'])

        expire_datetime = datetime.now() + timedelta(seconds=int(lk_request['expires_in']))

        setattr(request.user, request.user.social_fields["linkedin"]["token"], lk_request['access_token'])
        setattr(request.user, request.user.social_fields["linkedin"]["expire_datetime"], expire_datetime)

        request.user.save()

        return render(request, 'admin/self_closing.html')

    except Exception as e:
        data = dict()

        data["status"] = "error"
        data["error"] = str(e)
        data["feedname"] = request.user.username

        return JsonResponse(data)

def slack_callback(request):

    try:

        access_code = request.GET['code']

        sl_request = SlackAPI.get_authorized_tokens(access_code)

        if not sl_request['status']:
            raise Exception(request['error'])

        SlackIntegration.objects.create(
            user         = request.user,
            team_name    = sl_request["team_name"],
            access_token = sl_request["access_token"]
        )

        return render(request, 'admin/self_closing.html')

    except Exception as e:
        data = dict()

        data["status"] = "error"
        data["error"] = str(e)
        data["feedname"] = request.user.username

        return JsonResponse(data)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from datetime import timedelta

from oauth.twitterAPI  import TwitterAPI
from oauth.facebookAPI import FacebookAPI

def twitter_callback(request):

    try:

        oauth_verifier = request.GET['oauth_verifier']
        token          = request.session['OAUTH_TOKEN']
        token_secret   = request.session['OAUTH_TOKEN_SECRET']

        tw_request = TwitterAPI.get_authorized_tokens(oauth_verifier, token, token_secret)

        if not tw_request['status']:
            raise Exception(request['error'])

        setattr(request.user, request.user.social_fields["twitter"]["token"], tw_request['tokens']['oauth_token'])
        setattr(request.user, request.user.social_fields["twitter"]["secret"], tw_request['tokens']['oauth_token_secret'])

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
        expire_datetime = timezone.now() + timedelta(seconds=int(fb_request['token']['expires_in']))

        setattr(request.user, request.user.social_fields["facebook"]["token"], fb_request['token']['access_token'])
        setattr(request.user, request.user.social_fields["facebook"]["expire_datetime"], expire_datetime)

        request.user.save()

        return render(request, 'admin/self_closing.html')

    except Exception as e:
        data = dict()

        data["status"] = "error"
        data["error"] = str(e)
        data["feedname"] = request.user.username

        return JsonResponse(data)

    except Exception as e:
        data = dict()

        data["status"] = "error"
        data["error"] = str(e)
        data["feedname"] = request.user.username

        return JsonResponse(data)

def linkedin_callback(request):

    try:

        oauth_verifier = request.GET['oauth_verifier']

        tw_request = twitterAPI.get_authorized_tokens(oauth_verifier, token, token_secret)

        if not tw_request['status']:
            raise Exception(request['error'])

        request.user.twitter_token = tw_request['tokens']['oauth_token']
        request.user.twitter_token_secret = tw_request['tokens']['oauth_token_secret']

        request.user.save()

        return render(request, 'admin/self_closing.html')

    except Exception as e:
        data = dict()

        data["status"] = "error"
        data["error"] = str(e)
        data["feedname"] = request.user.username

        return JsonResponse(data)

def gplus_callback(request):

    try:

        oauth_verifier = request.GET['oauth_verifier']

        tw_request = twitterAPI.get_authorized_tokens(oauth_verifier, token, token_secret)

        if not tw_request['status']:
            raise Exception(request['error'])

        request.user.twitter_token = tw_request['tokens']['oauth_token']
        request.user.twitter_token_secret = tw_request['tokens']['oauth_token_secret']

        request.user.save()

        return render(request, 'admin/self_closing.html')

    except Exception as e:
        data = dict()

        data["status"] = "error"
        data["error"] = str(e)
        data["feedname"] = request.user.username

        return JsonResponse(data)

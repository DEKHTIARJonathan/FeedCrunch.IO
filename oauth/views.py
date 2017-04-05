#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import reverse
from django.http import JsonResponse
from django.shortcuts import render

import oauth.twitterAPI as twitterAPI

def twitter_callback(request):

    try:

        oauth_verifier = request.GET['oauth_verifier']
        token          = request.session['OAUTH_TOKEN']
        token_secret   = request.session['OAUTH_TOKEN_SECRET']

        tw_request = twitterAPI.get_authorized_tokens(oauth_verifier, token, token_secret)

        if not tw_request['status']:
            raise Exception(request['error'])

        request.user.twitter_token = tw_request['tokens']['oauth_token']
        request.user.twitter_token_secret = tw_request['tokens']['oauth_token_secret']

        request.user.save()

        return render(request, 'admin/self_closing.html')

    except Exception as e:
        data = {}

        data["status"] = "error"
        data["error"] = str(e)
        data["feedname"] = request.user.username

        return JsonResponse(data)

def facebook_callback(request):

    try:

        oauth_verifier = request.GET['oauth_verifier']
        token          = request.session['OAUTH_TOKEN']
        token_secret   = request.session['OAUTH_TOKEN_SECRET']

        tw_request = twitterAPI.get_authorized_tokens(oauth_verifier, token, token_secret)

        if not tw_request['status']:
            raise Exception(request['error'])

        request.user.twitter_token = tw_request['tokens']['oauth_token']
        request.user.twitter_token_secret = tw_request['tokens']['oauth_token_secret']

        request.user.save()

        return render(request, 'admin/self_closing.html')

    except Exception as e:
        data = {}

        data["status"] = "error"
        data["error"] = str(e)
        data["feedname"] = request.user.username

        return JsonResponse(data)

def linkedin_callback(request):

    try:

        oauth_verifier = request.GET['oauth_verifier']
        token          = request.session['OAUTH_TOKEN']
        token_secret   = request.session['OAUTH_TOKEN_SECRET']

        tw_request = twitterAPI.get_authorized_tokens(oauth_verifier, token, token_secret)

        if not tw_request['status']:
            raise Exception(request['error'])

        request.user.twitter_token = tw_request['tokens']['oauth_token']
        request.user.twitter_token_secret = tw_request['tokens']['oauth_token_secret']

        request.user.save()

        return render(request, 'admin/self_closing.html')

    except Exception as e:
        data = {}

        data["status"] = "error"
        data["error"] = str(e)
        data["feedname"] = request.user.username

        return JsonResponse(data)

def gplus_callback(request):

    try:

        oauth_verifier = request.GET['oauth_verifier']
        token          = request.session['OAUTH_TOKEN']
        token_secret   = request.session['OAUTH_TOKEN_SECRET']

        tw_request = twitterAPI.get_authorized_tokens(oauth_verifier, token, token_secret)

        if not tw_request['status']:
            raise Exception(request['error'])

        request.user.twitter_token = tw_request['tokens']['oauth_token']
        request.user.twitter_token_secret = tw_request['tokens']['oauth_token_secret']

        request.user.save()

        return render(request, 'admin/self_closing.html')

    except Exception as e:
        data = {}

        data["status"] = "error"
        data["error"] = str(e)
        data["feedname"] = request.user.username

        return JsonResponse(data)

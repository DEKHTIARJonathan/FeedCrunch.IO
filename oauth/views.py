# Create your views here.
# -*- coding:utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.conf import settings

from feedcrunch.models import FeedUser

from oauth import *

import tweepy

def get_callback(request):

    verifier = request.GET.get('oauth_verifier')

    auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    token = request.session.get('request_token')
    del request.session['request_token']
    auth.request_token = token

    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        raise Exception('Error! Failed to get access token.')

    request.session['key'] = auth.access_token
    request.session['secret'] = auth.access_token_secret

    usr_tmp = FeedUser.objects.get(username=request.user.username)

    usr_tmp.twitter_token = auth.access_token
    usr_tmp.twitter_token_secret = auth.access_token_secret

    usr_tmp.save()

    return HttpResponseRedirect(reverse('feedcrunch_rssadmin.views.index', kwargs={'feedname': request.user.username}))

def unlink(request):

    verifier = request.GET.get('oauth_verifier')

    auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    token = request.session.get('request_token')
    del request.session['request_token']
    auth.request_token = token

    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        raise Exception('Error! Failed to get access token.')

    request.session['key'] = auth.access_token
    request.session['secret'] = auth.access_token_secret

    usr_tmp = FeedUser.objects.get(username=request.user.username)

    usr_tmp.twitter_token = auth.access_token
    usr_tmp.twitter_token_secret = auth.access_token_secret

    usr_tmp.save()

    return HttpResponseRedirect(reverse('feedcrunch_rssadmin.views.index', kwargs={'feedname': request.user.username}))


def post(request):
    """
    Tweet
    """
    if request.method == 'POST':
        auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
        auth.set_access_token(request.session.get('key'), request.session.get('secret'))
        api = tweepy.API(auth_handler=auth)
        tweet = request.POST['tweet']
        api.update_status(tweet)
        return HttpResponse('Tweet complete!!')
    return HttpResponse('Error!!')

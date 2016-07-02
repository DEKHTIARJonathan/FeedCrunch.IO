# Create your views here.
# -*- coding:utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.conf import settings

from feedcrunch.models import FeedUser

from oauth import *
from twython import Twython

def get_callback(request):

    oauth_verifier = request.GET['oauth_verifier']

    twitter = Twython(settings.CONSUMER_KEY, settings.CONSUMER_SECRET, request.session['OAUTH_TOKEN'], request.session['OAUTH_TOKEN_SECRET'])

    """
    auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    token = request.session.get('request_token')
    del request.session['request_token']
    auth.request_token = token
    """

    try:
        final_step = twitter.get_authorized_tokens(oauth_verifier)
    except:
        raise Exception('Error! Failed to get access token.')

    usr_tmp = FeedUser.objects.get(username=request.user.username)

    usr_tmp.twitter_token = final_step['oauth_token']
    usr_tmp.twitter_token_secret = final_step['oauth_token_secret']

    usr_tmp.save()

    return HttpResponseRedirect(reverse('feedcrunch_rssadmin.views.index', kwargs={'feedname': request.user.username}))

def unlink(request):
    usr_tmp = FeedUser.objects.get(username=request.user.username)
    usr_tmp.reset_twitter_credentials()

    return HttpResponseRedirect(reverse('feedcrunch_rssadmin.views.index', kwargs={'feedname': request.user.username}))


def post(request):
    print "ok"
    """
    Tweet
    """
    """
    if request.method == 'POST':
        auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
        auth.set_access_token(request.session.get('key'), request.session.get('secret'))
        api = tweepy.API(auth_handler=auth)
        tweet = request.POST['tweet']
        api.update_status(tweet)
        return HttpResponse('Tweet complete!!')
    return HttpResponse('Error!!')
    """

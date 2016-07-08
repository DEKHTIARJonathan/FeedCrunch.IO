# Create your views here.
# -*- coding:utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from feedcrunch.models import FeedUser, Option

from .tw_funcs import *
from twython import Twython

def get_callback(request):

	try:

		oauth_verifier = request.GET['oauth_verifier']
		token = request.session['OAUTH_TOKEN']
		token_secret = request.session['OAUTH_TOKEN_SECRET']

		request = get_authorized_tokens(oauth_verifier, token, token_secret)

		if not request['status']:
			raise Exception(request['error'])

		usr_tmp = FeedUser.objects.get(username=request.user.username)

		usr_tmp.twitter_token = request['tokens']['oauth_token']
		usr_tmp.twitter_token_secret = request['tokens']['oauth_token_secret']

		usr_tmp.save()

		return HttpResponseRedirect(reverse('feedcrunch_rssadmin.views.index', kwargs={'feedname': request.user.username}))

	except Exception, e:
		return 'Error: ' + str(e)

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

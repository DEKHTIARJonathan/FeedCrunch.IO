# -*- coding: utf-8 -*-
from feedcrunch.models import *
from feedcrunch.model_files.models_options import *
from twython import Twython

import sys

class TwitterAPI(object):
	api = False
	error = ""
	maxsize_tweet = 140
	maxsize_hashtags = 27 # Allow to keep 85 char for the post title (95% of the post length is < 85 chars)
	length_link = 23
	baseurl = ""

	def __init__(self, user):

		try:
			twitter_consumer_key = Option.objects.get(parameter="twitter_consumer_key").value
			twitter_consumer_secret = Option.objects.get(parameter="twitter_consumer_secret").value

			if not user.is_twitter_enabled():
				raise ValueError("User has not enabled Twitter")
			else:
				self.api = Twython(twitter_consumer_key,
									twitter_consumer_secret,
									user.twitter_token,
									user.twitter_token_secret)

				self.baseurl = "https://www.feedcrunch.io/@"+user.username+"/redirect/"

		except Exception, e:
			self.error = str(e)
			self.api = False

	def connection_status(self):
		print self.error
		return bool(self.api)

	def post_twitter(self, title, id, tag_list=[]):

		if self.api != False:

			try:
				if isinstance(tag_list, list) and tag_list:
					hashtags = ""
					for tag in tag_list:

						if len(hashtags) + len(tag) + 1 < self.maxsize_hashtags:
							hashtags += "#" + tag + " "
						else:
							hashtags = hashtags[:-1]
							break

					if len(title) <= self.maxsize_tweet - (self.length_link + 1 + len(hashtags) + 1):
						self.api.update_status(status=title + ' ' + hashtags + ' ' + self.baseurl+str(id))

					else:
						title = title[: self.maxsize_tweet - (self.length_link + 1 + len(hashtags) + 1 + len(" [...]"))]
						self.api.update_status(status=title + ' [...] ' + hashtags + ' ' + self.baseurl+str(id))

					rslt = {'status':True}

				else:

					if len(title) <= self.maxsize_tweet - (self.length_link + 1):
						self.api.update_status(status=title + ' ' + self.baseurl+str(id))

					else:
						title = title[: self.maxsize_tweet - (self.length_link + 1 + len(" [...]"))]
						self.api.update_status(status=title + ' [...] ' + self.baseurl+str(id))

					rslt = {'status':True}

			except:
				rslt = {'status':False, 'error': sys.exc_info()[0]}

		else:
			rslt = {'status':False, 'error': "API Connection has failed during init phase"}

		return rslt

	def verify_credentials(self):
		if self.api != False:

			try:
				if self.api.verify_credentials()["screen_name"] != "":
					rslt = {'status': True}

				else:
					raise Exception("Credentials have not been verified")

			except:
				rslt = {'status':False, 'error': "Credentials have not been verified"}

		else:
			rslt = {'status':False, 'error': "API Connection has failed during init phase"}

		return rslt

#################### End of TwitterAPI ############################

def get_authorization_url(request):
	"""
	Twitter oauth authenticate
	"""
	try:
		try:
			twitter_consumer_key = Option.objects.get(parameter="twitter_consumer_key").value
			twitter_consumer_secret = Option.objects.get(parameter="twitter_consumer_secret").value

		except:
			raise Exception("Failed to retrieve the consumer keys.")

		twitter = Twython(twitter_consumer_key, twitter_consumer_secret)
		auth = twitter.get_authentication_tokens()

		try:
			auth_url = auth['auth_url']

		except tweepy.TweepError:
			raise Exception('Error! Failed to get request token.')

		request.session['OAUTH_TOKEN'] = auth['oauth_token']
		request.session['OAUTH_TOKEN_SECRET'] = auth['oauth_token_secret']

		return auth_url

	except Exception, e:
		return 'Error: ' + str(e)

def get_authorized_tokens(oauth_verifier, token, token_secret):
	try:
		try:
			twitter_consumer_key = Option.objects.get(parameter="twitter_consumer_key").value
			twitter_consumer_secret = Option.objects.get(parameter="twitter_consumer_secret").value

		except:
			return {'status':False, 'error': "Error! Failed to retrieve the consumer keys."}

		api = Twython(twitter_consumer_key, twitter_consumer_secret, token, token_secret)

		try:
			final_step = twitter.get_authorized_tokens(oauth_verifier)
			return {'status':True, 'tokens': final_step}

		except:
			return {'status':False, 'error':'Error! Failed to get access token.'}

	except Exception, e:
		return {'status':False, 'error': str(e)}

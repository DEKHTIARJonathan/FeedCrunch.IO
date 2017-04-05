#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from feedcrunch.models import *

import sys, facebook

class FacebookAPI(object):
    api = False
    error = ""

    def __init__(self, user):

        try:
            facebook_app_id     = Option.objects.get(parameter="facebook_app_id").value
            facebook_app_secret = Option.objects.get(parameter="facebook_app_secret").value

            '''
            if not user.is_social_network_enabled(network="twitter"):
                raise ValueError("User has not enabled Twitter")
            else:
                self.api = Twython(twitter_consumer_key,
                                    twitter_consumer_secret,
                                    user.twitter_token,
                                    user.twitter_token_secret)

                self.baseurl = "https://www.feedcrunch.io/@"+user.username+"/redirect/"
            '''

        except Exception as e:
            self.error = str(e)
            self.api = False


    def connection_status(self):
        print (self.error)
        return bool(self.api)

#################### End of FacebookAPI ############################

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

    except Exception as e:
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
            final_step = api.get_authorized_tokens(oauth_verifier)
            return {'status':True, 'tokens': final_step}

        except Exception as e:
            return {'status':False, 'error':'Error! Failed to get access token: ' + str(e)}

    except Exception as e:
        return {'status':False, 'error': str(e)}

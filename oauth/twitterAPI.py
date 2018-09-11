#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from feedcrunch.models import Option

from twython import Twython

class TwitterAPI(object):
    api               = False
    maxsize_tweet     = 140
    maxsize_hashtags  = 27 # Allow to keep 85 char for the post title (95% of the post length is < 85 chars)
    length_link       = 23
    baseurl           = ""

    def __init__(self, user):

        try:
            twitter_consumer_key    = Option.objects.get(parameter="twitter_consumer_key").value
            twitter_consumer_secret = Option.objects.get(parameter="twitter_consumer_secret").value

            if not user.is_social_network_enabled(network="twitter"):
                raise ValueError("User has not enabled Twitter")
            else:
                self.api = Twython(twitter_consumer_key,
                                    twitter_consumer_secret,
                                    user.twitter_token,
                                    user.twitter_token_secret)

                self.baseurl = "https://www.feedcrunch.io/@"+user.username+"/redirect/"

        except Exception as e:
            self.api = False

    def connection_status(self):
        return bool(self.api)

    def verify_credentials(self):
        try:
            if self.api == False:
                raise Exception("API Connection has failed during init phase")

            if self.api.verify_credentials()["screen_name"] != "":
                return {'status': True}

            else:
                raise Exception("Credentials are invalid")

        except Exception as e:
            return {'status':False, 'error': "TwitterAPI.verify_credentials(): " + str(e)}

    def get_hashtags_strings(self, tag_list, max_length = -1):

        hashtags = ""

        for tag in tag_list:

            if len(hashtags) + len(tag) + 1 < max(max_length,self.maxsize_hashtags):
                hashtags += "#" + tag + " "

            else:
                hashtags = hashtags[:-1]
                break

        return hashtags

    def publish_post(self, title, id, tag_list=[]):
        try:
            if self.api == False:
                raise Exception("API Connection has failed during init phase")

            if isinstance(tag_list, list):

                if tag_list: #  if tag_list is not empty

                    if len(title) < self.maxsize_tweet - self.length_link - self.maxsize_hashtags - 2: # we count two white space needed

                        # Title doesn't need to be modified, hashtags can be extended over the limit maxsize_hashtags but not over self.maxsize_tweet - self.length_link - len(title) - 2
                        hashtags = self.get_hashtags_strings(tag_list, self.maxsize_tweet - self.length_link - len(title) - 2)

                    else:

                        hashtags = self.get_hashtags_strings(tag_list)

                        if len(title) > self.maxsize_tweet - (self.length_link + len(hashtags) + 2):

                            # title need to be cutted accorded to the actual size of the hashtags
                            title = title[: self.maxsize_tweet - (self.length_link + len("[...]") + len(hashtags) + 3)] + " [...]" # 3 white space needed in total

                        # else the title doesn't need to be modified

                    status = title + ' ' + hashtags + ' ' + self.baseurl+str(id)

                else: # no hashtags precised

                    if len(title) > self.maxsize_tweet - (self.length_link + 1):

                        # title need to be cut : title = title[:140 - self.length_link - len("[…]")  - 2]

                        title = title[: self.maxsize_tweet - (self.length_link + len("[...]" + 2))] + " [...]"

                    # else nothing need to be changed at all !

                    status = title + " "  + self.baseurl+str(id)

                self.api.update_status(status=status)
                return {'status':True}

            else:
                raise ValueError("The Parameter 'tag_list' is not a list")

        except Exception as e:
            return {'status':False, 'error': "TwitterAPI.publish_post() - Error:" + str(e)}

    ##########################################################################################################
    # =========================================== STATIC METHODS =========================================== #
    ##########################################################################################################

    @staticmethod
    def get_authorization_url(request):
        """
        Twitter oauth authenticate
        """
        try:
            try:
                twitter_consumer_key    = Option.objects.get(parameter="twitter_consumer_key").value
                twitter_consumer_secret = Option.objects.get(parameter="twitter_consumer_secret").value

            except:
                raise Exception("Failed to retrieve the consumer keys.")

            try:
                auth = Twython(twitter_consumer_key, twitter_consumer_secret).get_authentication_tokens()
                auth_url = auth['auth_url']

            except Exception as e:
                raise Exception('Failed to get request token: %s' % str(e))

            request.session['OAUTH_TOKEN'] = auth['oauth_token']
            request.session['OAUTH_TOKEN_SECRET'] = auth['oauth_token_secret']

            return auth_url

        except Exception as e:
            return 'TwitterAPI.get_authorization_url() - Error: ' + str(e)

    @staticmethod
    def get_authorized_tokens(oauth_verifier, token, token_secret):
        try:
            try:
                twitter_consumer_key    = Option.objects.get(parameter="twitter_consumer_key").value
                twitter_consumer_secret = Option.objects.get(parameter="twitter_consumer_secret").value

            except:
                raise Exception("Failed to retrieve the consumer keys.")

            api = Twython(twitter_consumer_key, twitter_consumer_secret, token, token_secret)

            response = api.get_authorized_tokens(oauth_verifier)
            return {'status':True, 'oauth_token': response["oauth_token"], 'oauth_token_secret': response["oauth_token_secret"]}

        except Exception as e:
            return {'status':False, 'error':'TwitterAPI.get_authorized_tokens(): Error: ' + str(e)}

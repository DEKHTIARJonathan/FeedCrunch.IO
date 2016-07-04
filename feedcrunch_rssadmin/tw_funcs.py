# -*- coding: utf-8 -*-
from django.conf import settings
from feedcrunch.models import *
from twython import Twython

class TwitterAPI(object):
    api = False
    error = ""
    maxsize_tweet = 140
    length_link = 23
    baseurl = ""

    def __init__(self, user):

        try:
            if not user.is_twitter_enabled():
                raise ValueError("Your credentials are not valid")
            else:
                self.api = Twython(settings.CONSUMER_KEY,
                                        settings.CONSUMER_SECRET,
                                        user.twitter_token,
                                        user.twitter_token_secret)

                self.baseurl = "https://www.feedcrunch.io/@"+user.username+"/redirect/"

        except:
            self.error = "Your credentials are not valid"
            self.api = False


    def post_twitter(self, title, id):

        if len(title) <= self.maxsize_tweet - (self.length_link + 1):
            self.api.update_status(status=title + ' ' + self.baseurl+str(id))
        else:
            title = title[: self.maxsize_tweet - (self.length_link + 1 + len(" [...]"))]
            self.api.update_status(status=title + ' [...] ' + self.baseurl+str(id))

from feedcrunch.models import *
from twitter import Api

class TwitterAPI(object):
    api = False
    error = ""
    maxsize_tweet = 140
    length_link = 23
    baseurl = ""

    def __init__(self, user):
        self.api = Api(consumer_key=user.twitter_consummer_key,
                          consumer_secret=user.twitter_consummer_secret,
                          access_token_key=user.twitter_token,
                          access_token_secret=user.twitter_token_secret)
        try:
            if self.api.VerifyCredentials().id != 0:
                self.baseurl = "https://www.feedcrunch.io/@"+user.username+"/redirect/"

            else:
                raise ValueError("Your credentials are not valid")

        except:
            self.error = "Your credentials are not valid"
            self.api = False


    def post_twitter(self, title, id):

        if len(title) <= self.maxsize_tweet - (self.length_link + 1):
            self.api.PostUpdate(title + ' ' + self.baseurl+str(id))
        else:
            title = title[: self.maxsize_tweet - (self.length_link + 1 + len(" [...]"))]
            self.api.PostUpdate(title + ' [...] ' + self.baseurl+str(id))

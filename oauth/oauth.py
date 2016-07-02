from django.conf import settings
from twython import Twython

def get_authorization_url(request):
    """
    Twitter oauth authenticate
    """
    auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    try:
        auth_url = auth.get_authorization_url()
    except tweepy.TweepError:
        raise Exception('Error! Failed to get request token.')
    request.session['request_token'] = auth.request_token
    return auth_url

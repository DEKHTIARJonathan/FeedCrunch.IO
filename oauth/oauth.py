from django.conf import settings
from twython import Twython

def get_authorization_url(request):
    """
    Twitter oauth authenticate
    """
    twitter = Twython(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    auth = twitter.get_authentication_tokens()
    try:
        auth_url = auth['auth_url']
    except tweepy.TweepError:
        raise Exception('Error! Failed to get request token.')

    request.session['OAUTH_TOKEN'] = auth['oauth_token']
    request.session['OAUTH_TOKEN_SECRET'] = auth['oauth_token_secret']
    
    return auth_url

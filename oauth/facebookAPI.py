#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings

from feedcrunch.models import *

from urllib.parse import urlencode
from urllib.request import urlopen

import sys, facebook, json

class FacebookAPI(object):
    api = False
    error = ""
    callback_url = 'https://www.feedcrunch.io/oauth/facebook/get_callback/'
    callback_url_debug = 'http://local.feedcrunch.io:5000/oauth/facebook/get_callback/'
    app_permissions = [
        'public_profile',
        'user_about_me',
        'user_birthday',
        'email',
        'user_posts',
        'user_website',
        'publish_actions'
    ]

    def __init__(self):

        try:
            try:
                facebook_app_id     = Option.objects.get(parameter="facebook_app_id").value
                facebook_app_secret = Option.objects.get(parameter="facebook_app_secret").value

            except:
                raise Exception("FacebookAPI.__init__(): Failed to retrieve the Facebook Consumer Keys.")

            self.api = facebook.GraphAPI()
            self.api.access_token = self.api.get_app_access_token(facebook_app_id, facebook_app_secret)

        except Exception as e:
            self.error = str(e)
            self.api = False

    def connection_status(self):
        print (self.error)
        return bool(self.api)

    @staticmethod
    def get_authorization_url():
        """
        Facebook oauth authenticate
        """
        try:
            try:
                facebook_app_id = Option.objects.get(parameter="facebook_app_id").value
            except:
                raise Exception("FacebookAPI.get_authorization_url(): Failed to retrieve the Facebook App ID Key.")

            if settings.DEBUG:
                return facebook.auth_url(facebook_app_id, FacebookAPI.callback_url_debug, perms=FacebookAPI.app_permissions)
            else:
                return facebook.auth_url(facebook_app_id, FacebookAPI.callback_url, perms=FacebookAPI.app_permissions)


        except Exception as e:
            return 'Error: ' + str(e)


    @staticmethod
    def get_authorized_tokens(code):
        try:
            try:
                facebook_app_id     = Option.objects.get(parameter="facebook_app_id").value
                facebook_app_secret = Option.objects.get(parameter="facebook_app_secret").value

            except:
                return {'status':False, 'error': "Error! Failed to retrieve the consumer keys."}

            api = facebook.GraphAPI()

            try:
                if settings.DEBUG:
                    final_step = api.get_access_token_from_code(code=code, redirect_uri=FacebookAPI.callback_url_debug, app_id=facebook_app_id, app_secret=facebook_app_secret)
                else:
                    final_step = api.get_access_token_from_code(code=code, redirect_uri=FacebookAPI.callback_url, app_id=facebook_app_id, app_secret=facebook_app_secret)

                return {'status':True, 'token': final_step}

            except Exception as e:
                return {'status':False, 'error':'Error! Failed to get access token: ' + str(e)}

        except Exception as e:
            return {'status':False, 'error': str(e)}

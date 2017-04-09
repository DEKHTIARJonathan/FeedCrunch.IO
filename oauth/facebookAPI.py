#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings

from feedcrunch.models import *

import sys, facebook, json

class FacebookAPI(object):
    api = False
    error = ""
    post_illustration = "https://s3-eu-west-1.amazonaws.com/feedcrunch/static/home/images/social-share-images/social-img.png"
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
    baseurl = ""

    def __init__(self, user):

        try:
            if not user.is_social_network_enabled(network="facebook"):
                raise ValueError("User has not enabled Twitter")
            else:
                self.api = facebook.GraphAPI(user.facebook_access_token)
                self.baseurl = "https://www.feedcrunch.io/@"+user.username+"/redirect/"

        except Exception as e:
            self.error = str(e)
            self.api = False

    def connection_status(self):
        print (self.error)
        return bool(self.api)

    def verify_credentials(self):
        if self.api != False:

            try:
                facebook_app_id     = Option.objects.get(parameter="facebook_app_id").value
                facebook_app_secret = Option.objects.get(parameter="facebook_app_secret").value

            except:
                raise Exception("FacebookAPI.__init__(): Failed to retrieve the Facebook Consumer Keys.")

            try:
                '''
                {
                    'data':{
                        'app_id':'123456789',
                        'application':'Feedcrunch.io',
                        'expires_at':123456789,
                        'is_valid':True,
                        'issued_at':123456789,
                        'scopes':[
                            'user_birthday',
                            'user_website',
                            'user_about_me',
                            'user_posts',
                            'email',
                            'publish_actions',
                            'public_profile'
                        ],
                        'user_id':'123456789'
                    }
                }
                '''

                if self.api.debug_access_token(self.api.access_token, facebook_app_id, facebook_app_secret)["data"]["is_valid"]:
                    rslt = {'status': True}
                else:
                    raise Exception("Credentials have not been verified")

            except:
                rslt = {'status':False, 'error': "Credentials have not been verified"}

        else:
            rslt = {'status':False, 'error': "FacebookAPI.verify_credentials(): API Connection has failed during init phase"}

        return rslt

    def publish_post(self, title, id, tag_list=[]):

        if self.api != False:

            try:
                tag_str = ""
                if isinstance(tag_list, list) and tag_list: #  if tag_list is not empty:

                    for tag in tag_list:

                        if tag_str != "":
                            tag_str += " "

                        tag_str += "#"+tag

                message = title + " " + tag_str

                attach = {
                    "name": title,
                    "link": self.baseurl+str(id),
                    "caption": '',
                    "description": tag_str,
                    "picture" : self.post_illustration,
                }

                response = self.api.put_wall_post(message, attachment=attach)
                ## Response: {'id': '10211352122892746_10211354892441983'}
                rslt = {'status':True}

            except Exception as e:
                rslt = {'status':False, 'error': str(e)}

        else:
            rslt = {'status':False, 'error': "API Connection has failed during init phase"}

        return rslt

    ##########################################################################################################
    # =========================================== STATIC METHODS =========================================== #
    ##########################################################################################################

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
            facebook_app_id     = Option.objects.get(parameter="facebook_app_id").value
            facebook_app_secret = Option.objects.get(parameter="facebook_app_secret").value

        except:
            return {'status':False, 'error': "FacebookAPI.get_authorized_tokens(): Error! Failed to retrieve the consumer keys."}

        try:
            api = facebook.GraphAPI()

            if settings.DEBUG:
                final_step = api.get_access_token_from_code(code=code, redirect_uri=FacebookAPI.callback_url_debug, app_id=facebook_app_id, app_secret=facebook_app_secret)
            else:
                final_step = api.get_access_token_from_code(code=code, redirect_uri=FacebookAPI.callback_url, app_id=facebook_app_id, app_secret=facebook_app_secret)

            return {'status':True, 'token': final_step}

        except Exception as e:
            return {'status':False, 'error':'FacebookAPI.get_authorized_tokens(): Error! Failed to get access token: ' + str(e)}

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings

from feedcrunch.models import *

import facebook


class FacebookAPI(object):
    api                 = False
    post_illustration   = "https://s3-eu-west-1.amazonaws.com/feedcrunch/static/home/images/social-share-images/social-img.png"
    callback_url        = 'https://www.feedcrunch.io/oauth/facebook/get_callback/'
    callback_url_debug  = 'http://local.feedcrunch.io:5000/oauth/facebook/get_callback/'
    baseurl             = ''
    app_permissions = [
        'public_profile',
        'user_about_me',
        'user_birthday',
        'email',
        'user_posts',
        'user_website',
        'publish_actions'
    ]

    def __init__(self, user):

        try:
            if not user.is_social_network_enabled(network="facebook"):
                raise ValueError("User has not enabled Twitter")
            else:
                self.api = facebook.GraphAPI(user.facebook_access_token)
                self.baseurl = "https://www.feedcrunch.io/@"+user.username+"/redirect/"

        except Exception:
            self.api = False

    def connection_status(self):
        return bool(self.api)

    def verify_credentials(self):
        try:
            if self.api == False:
                raise Exception("API Connection has failed during init phase")

            try:
                facebook_app_id     = Option.objects.get(parameter="facebook_app_id").value
                facebook_app_secret = Option.objects.get(parameter="facebook_app_secret").value

            except:
                raise Exception("Failed to retrieve the Facebook Consumer Keys.")

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
                return {'status': True}
            else:
                raise Exception("Credentials have not been verified")

        except:
            return {'status':False, 'error': "FacebookAPI.verify_credentials(): Credentials have not been verified"}

    def publish_post(self, title, id, tag_list=None):

        if tag_list is None:
            tag_list = list()

        try:
            if not self.api:
                raise Exception("API Connection has failed during init phase")

            tag_str = ""

            if isinstance(tag_list, list) and tag_list:  # if tag_list is not empty:

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

            ## Response: {'id': '10211352122892746_10211354892441983'}
            response = self.api.put_wall_post(message, attachment=attach)

            return {'status': True}

        except Exception as e:
            return {
                'status': False,
                'error': 'FacebookAPI.publish_post() - Error: ' + str(e)
            }

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
                raise Exception("Failed to retrieve the Facebook App ID Key.")

            if settings.DEBUG or settings.TESTING:
                return facebook.auth_url(facebook_app_id, FacebookAPI.callback_url_debug, perms=FacebookAPI.app_permissions)
            else:
                return facebook.auth_url(facebook_app_id, FacebookAPI.callback_url, perms=FacebookAPI.app_permissions)

        except Exception as e:
            return 'FacebookAPI.get_authorization_url() - Error: ' + str(e)


    @staticmethod
    def get_authorized_tokens(code):
        try:
            try:
                facebook_app_id     = Option.objects.get(parameter="facebook_app_id").value
                facebook_app_secret = Option.objects.get(parameter="facebook_app_secret").value

            except:
                raise Exception("Failed to retrieve the consumer keys.")

            api = facebook.GraphAPI()

            if settings.DEBUG or settings.TESTING:
                response = api.get_access_token_from_code(code=code, redirect_uri=FacebookAPI.callback_url_debug, app_id=facebook_app_id, app_secret=facebook_app_secret)
            else:
                response = api.get_access_token_from_code(code=code, redirect_uri=FacebookAPI.callback_url, app_id=facebook_app_id, app_secret=facebook_app_secret)

            return {'status':True, 'access_token': response["access_token"], 'expires_in': response["expires_in"]}

        except Exception as e:
            return {'status':False, 'error':'FacebookAPI.get_authorized_tokens() - Error: ' + str(e)}

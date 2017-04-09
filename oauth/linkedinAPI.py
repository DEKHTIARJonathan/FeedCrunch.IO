#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings

from feedcrunch.models import *

import sys, json
from linkedin import linkedin

class LinkedInAPI(object):
    api = False
    error = ""
    post_illustration = "https://s3-eu-west-1.amazonaws.com/feedcrunch/static/home/images/social-share-images/social-img.png"
    callback_url = 'https://www.feedcrunch.io/oauth/linkedin/get_callback/'
    callback_url_debug = 'http://local.feedcrunch.io:5000/oauth/linkedin/get_callback/'
    app_permissions = [
        'r_basicprofile',
        'r_emailaddress',
        'rw_company_admin',
        'w_share',
        #'r_fullprofile',
        #'r_contactinfo'
    ]
    baseurl = ""

    def __init__(self, user):

        try:
            if not user.is_social_network_enabled(network="linkedin"):
                raise ValueError("User has not enabled Twitter")

            else:
                self.api = linkedin.LinkedInApplication(token=user.linkedin_access_token)
                self.baseurl = "https://www.feedcrunch.io/@"+user.username+"/redirect/"

        except Exception as e:
            self.error = str(e)
            self.api = False

    def connection_status(self):
        print (self.error)
        return bool(self.api)

    def verify_credentials(self):
        try:
            self.api.get_profile()
            return {'status': True}

        except:
            self.error = "LinkedInAPI: Credentials have not been verified"
            rslt = {'status': False, 'error': self.error}

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

                response = self.api.submit_share(
                        comment             = title + " " + tag_str,
                        title               = title,
                        description         = "Take RSS Feeds to the next level with Feedcrunch.io",
                        submitted_url       = self.baseurl+str(id),
                        submitted_image_url = self.post_illustration,
                        visibility_code     = 'anyone'
                )
                ## response: {"updateKey": "UPDATE-##-##", "updateUrl": "https://www.linkedin.com/updates?discuss=&scope=~##&stype=M&topic=###&type=U&a=reT3"}

                return {'status':True}

            except Exception as e:
                return {'status':False, 'error': str(e)}

        else:
            return {'status':False, 'error': "API Connection has failed during init phase"}

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
                linkedin_client_id     = Option.objects.get(parameter="linkedin_client_id").value
                linkedin_client_secret = Option.objects.get(parameter="linkedin_client_secret").value
            except:
                raise Exception("LinkedInAPI.get_authorization_url(): Failed to retrieve the LinkedIn App ID Key.")

            if settings.DEBUG:
                return linkedin.LinkedInAuthentication(linkedin_client_id, linkedin_client_secret, LinkedInAPI.callback_url_debug, LinkedInAPI.app_permissions).authorization_url
            else:
                return linkedin.LinkedInAuthentication(linkedin_client_id, linkedin_client_secret, LinkedInAPI.callback_url, LinkedInAPI.app_permissions).authorization_url


        except Exception as e:
            return 'Error: ' + str(e)


    @staticmethod
    def get_authorized_tokens(code):

        try:
            linkedin_client_id     = Option.objects.get(parameter="linkedin_client_id").value
            linkedin_client_secret = Option.objects.get(parameter="linkedin_client_secret").value
        except:
            return {'status':False, 'error': "LinkedInAPI.get_authorized_tokens(): Error! Failed to retrieve the consumer keys."}

        try:
            if settings.DEBUG:
                api = linkedin.LinkedInAuthentication(linkedin_client_id, linkedin_client_secret, LinkedInAPI.callback_url_debug, LinkedInAPI.app_permissions)
            else:
                api = linkedin.LinkedInAuthentication(linkedin_client_id, linkedin_client_secret, LinkedInAPI.callback_url, LinkedInAPI.app_permissions)

            api.authorization_code = code
            tmp_obj = api.get_access_token()

            final_step = {
                "access_token": tmp_obj.access_token,
                "expires_in": tmp_obj.expires_in
            }

            return {'status':True, 'token': final_step}

        except Exception as e:
            return {'status':False, 'error':'LinkedInAPI.get_authorized_tokens(): Error! Failed to get access token: ' + str(e)}

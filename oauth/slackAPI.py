#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings

from feedcrunch.models import *

import sys, json

from slacker import Slacker

class SlackAPI(object):
    api                 = False
    post_illustration   = 'https://s3-eu-west-1.amazonaws.com/feedcrunch/static/home/images/social-share-images/social-img.png'
    authorization_url   = 'https://slack.com/oauth/authorize?scope={0}&client_id={1}&redirect_uri={2}'
    callback_url        = 'https://www.feedcrunch.io/oauth/slack/get_callback/'
    callback_url_debug  = 'http://local.feedcrunch.io:5000/oauth/slack/get_callback/'
    baseurl             = ""
    app_permissions = [
        'channels:read',
        'chat:write:bot',
    ]

    def __init__(self, slackIntegrationObject):

        try:
            if not user.is_social_network_enabled(network="slack"):
                raise ValueError("User has not enabled Slack")

            else:
                self.api = Slacker(slackIntegrationObject.access_token)
                self.baseurl = "https://www.feedcrunch.io/@"+user.username+"/redirect/"

        except Exception as e:
            self.api = False

    def connection_status(self):
        return bool(self.api)

    def verify_credentials(self):
        try:
            self.api.users.identity()
            return {'status': True}

        except:
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
        Slack oauth authenticate
        """
        try:
            try:
                slack_client_id = Option.objects.get(parameter="slack_client_id").value
            except:
                raise Exception("Failed to retrieve the consumer keys.")

            if settings.DEBUG:
                return SlackAPI.authorization_url.format(
                    ",".join(SlackAPI.app_permissions),
                    slack_client_id,
                    SlackAPI.callback_url_debug
                )
            else:
                return SlackAPI.authorization_url.format(
                    ",".join(SlackAPI.app_permissions),
                    slack_client_id,
                    SlackAPI.callback_url
                )

        except Exception as e:
            return 'SlackAPI.get_authorization_url() - Error: ' + str(e)


    @staticmethod
    def get_authorized_tokens(code):

        try:

            try:
                slack_client_id     = Option.objects.get(parameter="slack_client_id").value
                slack_client_secret = Option.objects.get(parameter="slack_client_secret").value
            except:
                return {'status':False, 'error': "Failed to retrieve the consumer keys."}

            api = Slacker('')

            if settings.DEBUG:
                response = api.oauth.access(slack_client_id, slack_client_secret, code, redirect_uri=SlackAPI.callback_url_debug).body
            else:
                response = api.oauth.access(slack_client_id, slack_client_secret, code, redirect_uri=SlackAPI.callback_url).body

            return {'status':True, 'access_token': response["access_token"], 'team_name': response["team_name"]}

        except Exception as e:
            return {'status':False, 'error':'SlackAPI.get_authorized_tokens() - Error: ' + str(e)}

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
    channels            = None
    app_permissions = [
        'usergroups:read',  # Read all UserGroups
        'groups:read',      # Read Private Channels
        'channels:read',    # Read Public Channels
        'chat:write:bot',   # Post as Bot
    ]

    def __init__(self, slackIntegrationObject):

        try:
            '''
            if not slackIntegrationObject.user.is_social_network_enabled(network="slack"):
                raise ValueError("User has not enabled Slack")

            else:
                self.api     = Slacker(slackIntegrationObject.access_token)
                self.baseurl = "https://www.feedcrunch.io/@" + slackIntegrationObject.user.username + "/redirect/"
            '''
            self.api      = Slacker(slackIntegrationObject.access_token)
            self.baseurl  = "https://www.feedcrunch.io/@" + slackIntegrationObject.user.username + "/redirect/"
            self.channels = slackIntegrationObject.channels.split(",")

        except Exception as e:
            print (str(e))
            self.api = False

    def connection_status(self):
        return bool(self.api)

    def verify_credentials(self):
        try:
            if self.api == False:
                raise Exception("API Connection has failed during init phase")

            if self.api.auth.test().body["ok"] == True:
                return {'status': True}

            else:
                raise Exception("Credentials are invalid")

        except Exception as e:
            return {'status':False, 'error': "SlackAPI.verify_credentials(): " + str(e)}

    def get_available_channels(self):
        try:
            channels = list()

            for chan in self.api.channels.list().body["channels"]:
                if not chan["is_archived"]:
                    channels.append({
                        "name": chan["name_normalized"],
                        "public": True,
                        "active": self.is_channel_active(chan["name_normalized"]),
                    })

            for chan in self.api.groups.list().body["groups"]:
                if not chan["is_archived"] and not chan["is_mpim"]:
                    channels.append({
                        "name":   chan["name_normalized"],
                        "public": False,
                        "active": self.is_channel_active(chan["name_normalized"]),
                    })

            return {'status': True, 'channels': channels}

        except Exception as e:
            return {'status': False, 'error': "SlackAPI.get_available_channels() - Error:" + str(e)}

    def is_channel_active(self, channel_name):
        return channel_name in self.channels

    def publish_post(self, slackChannel, title, postID, tag_list=[]):
        try:
            if self.api == False:
                raise Exception("API Connection has failed during init phase")

            tag_str = ""
            if isinstance(tag_list, list) and tag_list: #  if tag_list is not empty:

                for tag in tag_list:

                    if tag_str != "":
                        tag_str += " "

                    tag_str += "#"+tag

            message = title + "\n" + tag_str + "\n\n" + self.baseurl+str(postID)

            self.api.chat.post_message('#'+slackChannel, message)

            return {'status':True}

        except Exception as e:
            return {'status':False, 'error': "SlackAPI.publish_post() - Error: "+str(e)}

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

            if settings.DEBUG or settings.TESTING:
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

            if settings.DEBUG or settings.TESTING:
                response = api.oauth.access(slack_client_id, slack_client_secret, code, redirect_uri=SlackAPI.callback_url_debug).body
            else:
                response = api.oauth.access(slack_client_id, slack_client_secret, code, redirect_uri=SlackAPI.callback_url).body

            return {'status':True, 'access_token': response["access_token"], 'team_name': response["team_name"]}

        except Exception as e:
            return {'status':False, 'error':'SlackAPI.get_authorized_tokens() - Error: ' + str(e)}

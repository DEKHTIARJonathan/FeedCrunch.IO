#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from feedcrunch.models import Post

from oauth.twitterAPI  import TwitterAPI
from oauth.facebookAPI import FacebookAPI
from oauth.linkedinAPI import LinkedInAPI
from oauth.slackAPI    import SlackAPI

from datetime import timedelta

####################################################################################################################
# ================================================== TWITTER  ==================================================== #
####################################################################################################################

def publish_on_twitter(idArticle):
    try:
        try:
            post = Post.objects.get(id=idArticle)
        except ObjectDoesNotExist:
            raise Exception("The given idArticle ('"+str(idArticle)+"') doesn't exist.")

        twitter_API = TwitterAPI(post.user)

        if twitter_API.connection_status():
            tag_list = [t.name for t in post.tags.all()]

            tw_rslt = twitter_API.publish_post(post.title, post.id, tag_list)

            if not tw_rslt['status']:
                raise Exception("An error occured in the twitter posting process: " + tw_rslt['error'])
        else:
            raise Exception("Not connected to the Twitter API")

    except Exception as e:
        raise Exception("task.publish_on_twitter - Error: " + str(e))

####################################################################################################################
# ================================================== Facebook  =================================================== #
####################################################################################################################

def publish_on_facebook(idArticle):
    try:
        try:
            post = Post.objects.get(id=idArticle)
        except ObjectDoesNotExist:
            raise Exception("The given idArticle ('" + str(idArticle) + "') doesn't exist.")

        facebook_API = FacebookAPI(post.user)

        if facebook_API.connection_status():
            tag_list = [t.name for t in post.tags.all()]

            fb_rslt = facebook_API.publish_post(post.title, post.id, tag_list)

            if not fb_rslt['status']:
                raise Exception("An error occured in the Facebook posting process: " + fb_rslt['error'])
        else:
            raise Exception("Not connected to the Facebook API")

    except Exception as e:
        raise Exception("task.publish_on_facebook - Error: " + str(e))

####################################################################################################################
# ================================================== LinkedIn  =================================================== #
####################################################################################################################

def publish_on_linkedin(idArticle):
    try:

        try:
            post = Post.objects.get(id=idArticle)
        except ObjectDoesNotExist:
            raise Exception("The given idArticle ('" + str(idArticle) + "') doesn't exist.")

        linkedin_API = LinkedInAPI(post.user)

        if linkedin_API.connection_status():
            tag_list = [t.name for t in post.tags.all()]
            lk_rslt = linkedin_API.publish_post(post.title, post.id, tag_list)

            if not lk_rslt['status']:
                raise Exception("An error occured in the linkedin posting process: " + lk_rslt['error'])
        else:
            raise Exception("Not connected to the LinkedIn API")

    except Exception as e:
        raise Exception("task.publish_on_linkedin - Error: " + str(e))

####################################################################################################################
# ==================================================== Slack  ==================================================== #
####################################################################################################################

def publish_on_slack(idArticle):
    try:
        try:
            post = Post.objects.get(id=idArticle)
        except ObjectDoesNotExist:
            raise Exception("The given idArticle ('" + str(idArticle) + "') doesn't exist.")

        for slack_instance in post.user.rel_slack_integrations.all():
            slack_API = SlackAPI(slack_instance)

            if slack_API.connection_status():
                tag_list = [t.name for t in post.tags.all()]

                for channel in slack_instance.channels.split(","):

                    sl_rslt = slack_API.publish_post(channel, post.title, post.id, tag_list)
                    if not sl_rslt['status']:
                        raise Exception("An error occured in the slack posting process: " + sl_rslt['error'])
            else:
                raise Exception("Not connected to the Slack API")

    except Exception as e:
        raise Exception("task.publish_on_slack - Error: " + str(e))

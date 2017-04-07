#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from feedcrunch.models import Post

from oauth.twitterAPI import TwitterAPI
from oauth.facebookAPI import FacebookAPI

from datetime import timedelta

def publish_on_twitter(idArticle):
    try:
        post = Post.objects.get(id=idArticle)
    except ObjectDoesNotExist:
        raise Exception("task.publish_on_twitter: The given idArticle ('"+str(idArticle)+"') doesn't exist.")

    twitter_API = TwitterAPI(post.user)

    if twitter_API.connection_status():
        tag_list = [t.name for t in post.tags.all()]

        if not twitter_API.publish_post(post.title, post.id, tag_list)['status']:
            raise Exception("task.publish_on_twitter: An error occured in the twitter posting process: " + tw_rslt['error'])
    else:
        raise Exception("task.publish_on_twitter: Not connected to the Twitter API")

def publish_on_facebook(idArticle):
    try:
        post = Post.objects.get(id=idArticle)
    except ObjectDoesNotExist:
        raise Exception("task.publish_on_facebook: The given idArticle ('"+str(idArticle)+"') doesn't exist.")

    facebook_API = FacebookAPI(post.user)

    if facebook_API.connection_status():
        tag_list = [t.name for t in post.tags.all()]

        if not facebook_API.publish_post(post.title, post.id, tag_list)['status']:
            raise Exception("task.publish_on_facebook: An error occured in the twitter posting process: " + tw_rslt['error'])
    else:
        raise Exception("task.publish_on_facebook: Not connected to the Twitter API")

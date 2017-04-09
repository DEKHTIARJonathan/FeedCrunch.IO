#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from feedcrunch.models import FeedUser

def auto_format_social_network(social_network=None):

    if social_network is None:
        raise Exception("'social_network' is none.")
    elif not isinstance(social_network, str):
        raise Exception("'social_network' is not a string.")
    else:
        social_network = social_network.lower()

    if social_network not in FeedUser.social_fields.keys():
        raise Exception("'social_network' (" + social_network + ") is not supported.")
    else:
        return social_network

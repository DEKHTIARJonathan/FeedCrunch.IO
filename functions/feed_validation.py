#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import feedparser


def validate_feed(feed):
    if isinstance(feed, str):
        feed = feedparser.parse(feed)

    elif not isinstance(feed, feedparser.FeedParserDict):
        raise Exception("Not a string or a feedparser.FeedParserDict instance.")

    if feed.bozo == 0:
        return True

    elif 'status' in feed and feed["status"] == 200:
        return True

    else:
        return False

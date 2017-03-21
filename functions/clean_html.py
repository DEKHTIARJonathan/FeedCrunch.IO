#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import re, unicodedata
from html.parser import HTMLParser

def clean_html(raw_html):
	# Normalizarion
	if isinstance(raw_html, str):
		cleantext = unicodedata.normalize('NFC', raw_html)

	# Removing all HTML Tags
	cleanr = re.compile('<.*?>')
	cleantext = re.sub(cleanr, '', cleantext)

	# Remove all HTML Codes and convert them to string
	cleantext = HTMLParser().unescape(cleantext)

	return cleantext

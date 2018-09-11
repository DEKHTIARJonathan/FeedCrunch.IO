#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import re
import unicodedata
import html

def clean_html(raw_html):
    # Normalizarion
    cleantext = unicodedata.normalize('NFC', raw_html)

    # Removing all HTML Tags
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', cleantext)

    # Remove all HTML Codes and convert them to string
    return html.unescape(cleantext)

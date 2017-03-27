#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import re

def format_title(title):
    stopwords = 'a an and at but by for in nor of on or so the to up yet'.split(' ')

    if isinstance(title, str):
        title = title.replace("–", "-") #en dash
        title = title.replace("\u2013", "-") #en dash
        title = title.strip().lower()

        rslt = ""
        for word in title.split(' '):
            if word not in stopwords:
                word = word.capitalize()

            if rslt != "":
                rslt += " "

            rslt += word

        rslt = re.sub(' +',' ',rslt)

        output = rslt[0].capitalize()+rslt[1:]

        return output

    else:
        raise ValueError("This datatype ( "+ type(title) +" ) is not handled by the application.")

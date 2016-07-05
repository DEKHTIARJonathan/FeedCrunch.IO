# -*- coding: utf-8 -*-
import re

def format_title(title):
    stopwords = 'a an and at but by for in nor of on or so the to up yet'.split(' ')

    if type(title) is unicode:
        title = title.encode('utf-8','ignore')

    if type(title) is str:
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

        return rslt

    else:
        raise ValueError("This datatype ( "+ type(title) +" ) is not handled by the application.")

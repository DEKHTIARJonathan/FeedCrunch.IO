#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render
from feedcrunch.models import FeedUser, Post, Option

def myrender(request, template, dictionary={}):
	dictionary.update({'template_name': template})
	dictionary.update({'user_count': FeedUser.objects.count()})
	dictionary.update({'post_count': Post.objects.count()})

	if Option.objects.filter(parameter="display_user_count").exists():
		dictionary.update({'display_user_count': Option.objects.get(parameter="display_user_count").get_bool_value()})
	else:
		dictionary.update({'display_user_count':False})

	return render(request, template, dictionary)

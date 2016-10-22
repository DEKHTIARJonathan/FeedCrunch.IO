#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect

def check_admin(feedname, user):
	if feedname == None:
		return HttpResponse("Error")

	elif not user.is_authenticated():
		return HttpResponseRedirect('/login')

	elif not user.is_active:
		return HttpResponse("We are sorry... You account is inactive. Please contact our support")

	elif feedname != user.username:
		return HttpResponseRedirect('/@'+user.username+'/admin')

	else:
		return True

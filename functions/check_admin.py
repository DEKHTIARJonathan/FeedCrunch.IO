#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect

def check_admin(feedname, user, bypassOnboarding = False):
	if feedname == None:
		return HttpResponse("Error")

	elif not user.is_authenticated():
		return HttpResponseRedirect('/login')

	elif not user.is_active:
		return HttpResponse("We are sorry... You account is inactive. Please contact our support")

	elif feedname != user.username:
		return HttpResponseRedirect('/@'+user.username+'/admin')

	elif user.onboarding_done and bypassOnboarding:
		return HttpResponseRedirect('/@'+user.username+'/admin')

	else:
		return True

'''
elif not (user.onboarding_done or bypassOnboarding):
	return HttpResponseRedirect('/@'+user.username+'/admin/onboarding/')
'''

def check_admin_api(user):

	if not user.is_authenticated():
		return 'User Not authenticated'

	elif not user.is_active:
		return "We are sorry... You account is inactive. Please contact our support"

	else:
		return True

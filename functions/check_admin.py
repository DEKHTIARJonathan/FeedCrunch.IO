#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import HttpResponse
from django.http import HttpResponseRedirect


def check_admin(feedname, user, bypassOnboardingCheck = False):
    if feedname == None:
        return HttpResponse("Error")

    elif not user.is_authenticated:
        return HttpResponseRedirect('/login/')

    elif not user.is_active:
        return HttpResponse("We are sorry... You account is inactive. Please contact our support")

    elif feedname != user.username:
        return HttpResponseRedirect('/@'+user.username+'/admin/')

    elif (not user.onboarding_done) and (not bypassOnboardingCheck):
        return HttpResponseRedirect('/@'+user.username+'/admin/onboarding/')

    else:
        return True


def check_admin_api(user):

    if not user.is_authenticated:
        return 'User Not authenticated'

    elif not user.is_active:
        return "We are sorry... You account is inactive. Please contact our support"

    else:
        return True

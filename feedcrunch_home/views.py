#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext, loader

from rest_framework.authtoken.models import Token

from feedcrunch.models import Country, Option, FeedUser

from custom_render import myrender as render

def index(request):
    try:
        freemium_period = Option.objects.get(parameter="freemium_period").get_bool_value()
    except:
        print ("freemium_period may not exists.")
        freemium_period = True

    return render(request, 'home.html', {'free_period': freemium_period})

def faq(request):
    return render(request, 'faq.html', {})

def contact(request):
    return render(request, 'contact.html', {})

def about(request):
    return render(request, 'about.html', {})

def terms(request):
    return render(request, 'terms.html', {})

def loginView(request):
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/@'+request.user.username+'/admin')

        else:
            return HttpResponseRedirect('/login/')
    else:
        if request.user.is_authenticated():
            return HttpResponseRedirect('/@'+request.user.username+'/admin')
        else:
            return render(request, 'login.html', {})

def signUPView(request):

    if request.method == 'POST':

        username = request.POST['username'].lower()
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        gender = request.POST['gender']
        country = request.POST['country']
        password = request.POST['password']
        birthdate = request.POST['birthdate']

        tmp_usr = FeedUser.objects.create_user(
            username,
            email,
            password,
            firstname=firstname,
            lastname=lastname,
            country=country,
            gender=gender,
            birthdate=birthdate
        )

        user = authenticate(username=username, password=password)
        login(request, user)

        # We create an associated token for the user
        Token.objects.create(user=user)

        return HttpResponseRedirect('/@'+request.user.username+'/admin')

    else:

        if request.user.is_authenticated():
            return HttpResponseRedirect('/@'+request.user.username+'/admin')
        else:
            country_list = Country.objects.all().order_by('name')
            return render(request, 'signup.html', {'countries': country_list})

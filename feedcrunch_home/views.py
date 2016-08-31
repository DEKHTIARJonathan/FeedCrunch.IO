#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from feedcrunch.models import Country, Option, FeedUser

from feedcrunch_home.myutils import myrender as render

def index(request):
	try:
		freemium_period = Option.objects.get(parameter="freemium_period").get_bool_value()
	except:
		print "freemium_period may not exists."
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
	context = RequestContext(request)
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/@'+request.user.username+'/admin')

			else:
				return HttpResponse("Your account is inactive.")
		else:
			return HttpResponseRedirect('/login/')
	else:
		if request.user.is_authenticated():
			return HttpResponseRedirect('/@'+request.user.username+'/admin')
		else:
			return render(request, 'login.html', {})

def signUPView(request):

	if request.method == 'POST':
		try:
			username = request.POST['username']
			firstname = request.POST['firstname']
			lastname = request.POST['lastname']
			email = request.POST['email']
			gender = request.POST['gender']
			country = request.POST['country']
			password = request.POST['password']
			birthdate = request.POST['birthdate']

			tmp_usr = FeedUser.objects.create_user(username, email, password, firstname, lastname, country, gender, birthdate)

			user = authenticate(username=username, password=password)
			login(request, user)

			return HttpResponseRedirect('/@'+request.user.username+'/admin')

		except Exception, e:
			return HttpResponse(str(e))
	else:

		if request.user.is_authenticated():
			return HttpResponseRedirect('/@'+request.user.username+'/admin')
		else:
			country_list = Country.objects.all().order_by('name')
			return render(request, 'signup.html', {'countries': country_list})

#@login_required(login_url='/login/')
def test(request):
	return HttpResponse("Welcome.")

def handler404(request):
	response = render_to_response('404.html')
	response.status_code = 404
	return response

def handler500(request):
	response = render_to_response('500.html')
	response.status_code = 500
	return response

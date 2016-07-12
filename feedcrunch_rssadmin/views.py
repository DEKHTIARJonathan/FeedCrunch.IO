# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from feedcrunch.models import Post, FeedUser, Country
from twitter.tw_funcs import TwitterAPI, get_authorization_url

from .ap_style import format_title

import json

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

def str2bool(v):
	return v.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']

# Create your views here.

def index(request, feedname=None):

	check_passed = check_admin(feedname, request.user)
	if check_passed != True:
		return check_passed
	else:
		if not request.user.is_twitter_activated():
			auth_url = get_authorization_url(request)
		else:
			auth_url = False # False => Don't need to authenticate with Twitter

		country_list = Country.objects.all().order_by('name')

		return render(request, 'admin_index.html', {'auth_url': auth_url, 'countries': country_list})

def add_form(request, feedname=None):

	check_passed = check_admin(feedname, request.user)
	if check_passed != True:
		return check_passed
	else:
		return render(request, 'post_form.html')

def update_password(request, feedname=None):

	data = {}
	data["operation"] = "update_password"

	if request.method == 'POST':

		if check_admin(feedname, request.user) != True:
			data["status"] = "error"
			data["error"] = "You are not allowed to perform this action"
			data["feedname"] = str(feedname)
		else:
			try:
				password1 = request.POST["password1"]
				password2 = request.POST["password2"]

				if password1 != password2:
					raise ValueError("The given passwords are different.")
				else:

					tmp_user = FeedUser.objects.get(username=request.user.username)

					FeedUser.objects._validate_password(password1)

					tmp_user.set_password(password1)
					tmp_user.save()

					return HttpResponseRedirect('/@'+request.user.username+'/admin')

			except Exception, e:
				data["status"] = "error"
				data["error"] = "An error occured in the process: " + str(e)
				data["feedname"] = feedname

	else:
		data["status"] = "error"
		data["error"] = "Only available with a POST Request"
		data["feedname"] = feedname

	return JsonResponse(data)

def social_links_edit(request, feedname=None):

	val = URLValidator()

	data = {}
	data["operation"] = "social_links_edit"

	if request.method == 'POST':

		if check_admin(feedname, request.user) != True:
			data["status"] = "error"
			data["error"] = "You are not allowed to perform this action"
			data["feedname"] = str(feedname)
		else:
			try:
				social_networks = [
					'twitter',
					'facebook',
					'pinterest',
					'gplus',
					'dribbble',
					'linkedin',
					'flickr',
					'git',
					'vimeo',
					'stumble',
					'instagram',
					'youtube',
					'researchgate',
					'website',
					'blog'
				]

				social_data = {}
				for social in social_networks:
					url = request.POST[social]
					if url != '':
						val(url) #Raise a ValidationError if the URL is invalid.
					social_data[social] = url

				tmp_user = FeedUser.objects.get(username=request.user.username)

				tmp_user.social_twitter = social_data['twitter']
				tmp_user.social_facebook = social_data['facebook']
				tmp_user.social_pinterest = social_data['pinterest']
				tmp_user.social_gplus = social_data['gplus']
				tmp_user.social_dribbble = social_data['dribbble']
				tmp_user.social_linkedin = social_data['linkedin']
				tmp_user.social_flickr = social_data['flickr']
				tmp_user.social_stumble = social_data['stumble']
				tmp_user.social_vimeo = social_data['vimeo']
				tmp_user.social_instagram = social_data['instagram']
				tmp_user.social_youtube = social_data['youtube']
				tmp_user.social_researchgate = social_data['researchgate']
				tmp_user.social_personalwebsite = social_data['website']
				tmp_user.social_blog = social_data['blog']
				tmp_user.social_git = social_data['git']

				tmp_user.save()

				return HttpResponseRedirect('/@'+request.user.username+'/admin')

			except Exception, e:
				data["status"] = "error"
				data["error"] = "An error occured in the process: " + str(e)
				data["feedname"] = feedname

	else:
		data["status"] = "error"
		data["error"] = "Only available with a POST Request"
		data["feedname"] = feedname

	return JsonResponse(data)

def add_form_ajax(request, feedname=None):

	data = {}
	data["operation"] = "insert"

	if request.method == 'POST':

		if check_admin(feedname, request.user) != True:
			data["status"] = "error"
			data["error"] = "You are not allowed to perform this action"
			data["postID"] = str(postID)
		else:
			try:

				title = request.POST['title']
				link = request.POST['link']

				activated_bool = str2bool(request.POST['activated'])
				twitter_bool = str2bool(request.POST['twitter'])

				if str2bool(request.POST['autoformat']) :
					title = format_title(title)

				if title == "" or link == "":
					data["status"] = "error"
					data["error"] = "Title and/or Link is/are issing"
					data["postID"] = str(postID)
				else:
					tmp_user = FeedUser.objects.get(username=request.user.username)

					tmp_post = Post.objects.create(title=title, link=link, clicks=0, user=tmp_user, activeLink=activated_bool)
					tmp_post.save()

					if twitter_bool and tmp_user.is_twitter_enabled():

							twitter_instance = TwitterAPI(tmp_user)

							if twitter_instance.connection_status():
								tmp_post.save()
								twitter_instance.post_twitter(title, tmp_post.id)
								data["status"] = "success"
								data["postID"] = str(tmp_post.id)

							else:
								raise Exception("Not connected to the Twitter API")

					else:
						tmp_post.save()
						data["status"] = "success"
						data["postID"] = str(tmp_post.id)

			except Exception, e:
				data["status"] = "error"
				data["error"] = "An error occured in the process: " + str(e)
				data["postID"] = None

	else:
		data["status"] = "error"
		data["error"] = "Only available with a POST Request"
		data["postID"] = str(postID)

	return JsonResponse(data)

def modify_form_ajax(request, feedname=None, postID=None):

	data = {}
	data["operation"] = "modification"

	if request.method == 'POST':

		if check_admin(feedname, request.user) != True:
			data["status"] = "error"
			data["error"] = "You are not allowed to perform this action"
			data["postID"] = str(postID)

		elif postID == None:
			data["status"] = "error"
			data["error"] = "postID parameter is missing"
			data["postID"] = ""

		else:
			try:
				title = request.POST['title']
				link = request.POST['link']

				activated_bool = str2bool(request.POST['activated'])
				twitter_bool = str2bool(request.POST['twitter'])

				if str2bool(request.POST['autoformat']) :
					title = format_title(title)

				if title == "" or link == "":
					raise Exception("Data Missing")

				post = Post.objects.get(id=postID, user=feedname)

				post.title = title
				post.link = link
				post.activeLink = activated_bool

				tmp_user = FeedUser.objects.get(username=feedname)
				if twitter_bool and tmp_user.is_twitter_enabled():

						twitter_instance = TwitterAPI(tmp_user)

						if twitter_instance.connection_status():
							post.save()
							twitter_instance.post_twitter(title, postID)
							data["status"] = "success"
							data["postID"] = str(postID)

						else:
							raise Exception("Not connected to the Twitter API")

				else:
					post.save()
					data["status"] = "success"
					data["postID"] = str(postID)


			except Exception, e:
				data["status"] = "error"
				data["error"] = str(e)
				data["postID"] = str(postID)

	else:
		data["status"] = "error"
		data["error"] = "Only available with a POST Request"
		data["postID"] = str(postID)

	return JsonResponse(data)

def modify_listing(request, feedname=None):

	check_passed = check_admin(feedname, request.user)
	if check_passed != True:
		return check_passed
	else:
		posts = Post.objects.filter(user = feedname).order_by('-id')
		return render(request, 'listing.html', {'posts': posts})

def modify_form(request, feedname=None, postID=None):

	check_passed = check_admin(feedname, request.user)
	if check_passed != True:
		return check_passed

	elif postID == None:
		return HttpResponseRedirect("/@"+feedname+"/admin/modify")

	else:
		try:
			post = Post.objects.get(id=postID, user=feedname)
			return render(request, 'post_form.html', {"post": post})

		except:
			return HttpResponseRedirect("/@"+feedname+"/admin/modify")


def delete_ajax(request, feedname=None):

	data = {}
	data["operation"] = "delete"

	if request.method == 'POST':

		if check_admin(feedname, request.user) != True:
			data["status"] = "error"
			data["error"] = "You are not allowed to perform this action"
			data["postID"] = str(postID)
		else:
			try:
				postID = int(request.POST['postID'])

				if type(postID) is not int or postID < 1:
					data["status"] = "error"
					data["error"] = "postID parameter is not valid"
					data["postID"] = str(postID)

				else:

					Post.objects.filter(id=postID, user=feedname).delete()
					data["status"] = "success"
					data["postID"] = str(postID)

			except:
				data["status"] = "error"
				data["error"] = "An error occured in the process"
				data["postID"] = str(postID)


	else:
		data["status"] = "error"
		data["error"] = "Only available with a POST Request"
		data["postID"] = str(postID)

	return JsonResponse(data)


def delete_listing(request, feedname=None):

	check_passed = check_admin(feedname, request.user)
	if check_passed != True:
		return check_passed
	else:
		posts = Post.objects.filter(user = feedname).order_by('-id')
		return render(request, 'listing.html', {'posts': posts})

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext, loader

import sys, os

from mimetypes import MimeTypes

from feedcrunch.models import Post, FeedUser

from custom_render import myrender as render
from rss_generator import generateRSS

# Create your views here.

def index(request, feedname=None):

	if feedname == None or (not FeedUser.objects.filter(username = feedname).exists()):
		return HttpResponseRedirect("/")

	else:
		posts = Post.objects.filter(user = feedname, activeLink=True).order_by('-id')
		requested_user = FeedUser.objects.get(username=feedname)
		return render(request, 'rssviewer.html', {'posts': posts, 'requested_user': requested_user})

def dataset(request, feedname=None):

	if feedname == None or (not FeedUser.objects.filter(username = feedname).exists()):
		return HttpResponseRedirect("/")

	elif not request.user.is_superuser:
		return HttpResponseRedirect("/@"+feedname)

	else:
		posts = Post.objects.filter(user = feedname, activeLink=True).order_by('id')
		data_output = ""

		for post in posts:

			data_output += str(post.id) + "|" + post.title + "|" + post.link + "|" + post.get_domain() + "<br/>"

		return HttpResponse(data_output)

def search(request, feedname=None):
	result = {}

	if feedname == None or (not FeedUser.objects.filter(username = feedname).exists()):
		return HttpResponseRedirect("/")

	elif request.method == 'POST':
		search_str = request.POST['search_str']

		if search_str != "":
			rslt_from_db = Post.objects.filter(title__icontains=search_str, user=feedname, activeLink=True).order_by('-id')
		else:
			rslt_from_db = Post.objects.filter(user=feedname).order_by('-id')

		posts = []

		for post in rslt_from_db:
			data = {}
			data["id"] = post.id
			data["title"] = post.title
			data["when"] = post.get_date()
			data["domain_name"] = post.get_domain()
			posts.append(data)

		result["status"] = "OK"
		result["posts"] = posts

	else:

		result["status"] = "KO"
		result["posts"] = {}

	result["search_str"] = search_str
	return JsonResponse(result)

def redirect(request, feedname=None, postID=None):
	if postID == None or feedname == None :
		return HttpResponse("Error")
	else:
		try:
			post = Post.objects.get(id=postID, user=feedname, activeLink=True)

			post.clicks += 1
			post.save()

			return HttpResponseRedirect(post.link)
		except:
			return HttpResponseRedirect("/@"+feedname)

def rss_feed(request, feedname=None):
	if feedname == None:
		return HttpResponse("Error")
	else:
		if Post.objects.filter(user=feedname).count() > 0:
			fg = generateRSS("rss", feedname)
			return HttpResponse(fg.rss_str(pretty=True, encoding='UTF-8'), content_type='application/xml')
		else:
			return HttpResponse("No Entries in this feed yet")

def atom_feed(request, feedname=None):
	if feedname == None:
		return HttpResponse("Error")
	else:
		if Post.objects.filter(user=feedname).count() > 0:
			fg = generateRSS("atom", feedname)
			return HttpResponse(fg.atom_str(pretty=True, encoding='UTF-8'), content_type='application/xml')
		else:
			return HttpResponse("No Entries in this feed yet")

'''

from django.core.files import File
from django_downloadview.exceptions import FileNotFound
from django_downloadview import BaseDownloadView

class PathDownloadView(BaseDownloadView):
	"""Serve a file using filename."""
	#: Server-side name (including path) of the file to serve.
	#:
	#: Filename is supposed to be an absolute filename of a file located on the
	#: local filesystem.
	path = None

	def get_path(self):
		"""Return actual path of the file to serve.
		Default implementation simply returns view's :py:attr:`path`.
		Override this method if you want custom implementation.
		As an example, :py:attr:`path` could be relative and your custom
		:py:meth:`get_path` implementation makes it absolute.
		"""
		return self.path

	def get_file(self):
		"""Use path to return wrapper around file to serve."""
		filename = self.get_path()
		if not os.path.isfile(filename):
			raise FileNotFound('File "{0}" does not exists'.format(filename))
		return File(open(filename, 'rb'))

	def get_mimetype(self):
		filename = self.get_path()
		mime = MimeTypes()
		mime_type = mime.guess_type(filename)
		return mime_type[0]


def photo(request, feedname=None):
	if feedname == None or (not FeedUser.objects.filter(username = feedname).exists()):
		OPENID_LOGO_BASE_64 = """R0lGODlhAQABAIAAAP==""" #Smallest GIF as Possible : transparent image 1x1
		return HttpResponse(OPENID_LOGO_BASE_64.decode('base64'), content_type='image/gif')

	else:
		requested_user = FeedUser.objects.get(username=feedname)

		if settings.DEBUG:
			pathdownloader = PathDownloadView()
			pathdownloader.path = os.path.join(settings.MEDIA_ROOT, str(requested_user.profile_picture))

			return HttpResponse(pathdownloader.get_file(), content_type=pathdownloader.get_mimetype())
		else:
			photo_url = "https://%s/%s/%s" % (settings.AWS_S3_CUSTOM_DOMAIN, settings.MEDIAFILES_LOCATION, requested_user.profile_picture)
			return HttpResponseRedirect(photo_url)
'''

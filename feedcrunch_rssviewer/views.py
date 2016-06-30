# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import authenticate, login, logout

from feedcrunch.models import Post, FeedUser

from feedgen.feed import FeedGenerator
from .functions import *

# Create your views here.

def index(request, feedname=None):

    if feedname == None or (not FeedUser.objects.filter(username = feedname).exists()):
        return HttpResponseRedirect("/")

    else:
        posts = Post.objects.filter(user = feedname).order_by('-id')
        return render(request, 'index.html', {'posts': posts})


def search(request, feedname=None):

    if feedname == None or (not FeedUser.objects.filter(username = feedname).exists()):
        return HttpResponseRedirect("/")

    elif request.method == 'POST':
        search_str = request.POST['search_str']

        if search_str != "":

            posts = []

            for post in Post.objects.filter(title__icontains=search_str).order_by('-id'):
                data = {}
                data["id"] = post.id
                data["title"] = post.title
                data["when"] = post.get_date()
                data["domain_name"] = post.get_domain()
                posts.append(data)

            result = {}
            result["status"] = "OK"
            result["search_str"] = search_str
            result["posts"] = posts

    else:
        result = {}
        result["status"] = "KO"
        result["search_str"] = search_str
        result["posts"] = {}

    return JsonResponse(result)


def redirect(request, feedname=None, postID=None):
    if postID == None or feedname == None :
        return HttpResponse("Error")
    else:
        try:
            post = Post.objects.get(id=postID, user=feedname)
            return HttpResponseRedirect(post.link)
        except:
            return HttpResponseRedirect("/@"+feedname)

def rss_feed(request, feedname=None):
    if feedname == None:
        return HttpResponse("Error")
    else:
        if Post.objects.count() > 0:
            fg = generateRSS("rss")
            return HttpResponse(fg.rss_str(pretty=True, encoding='UTF-8'), content_type='application/xml')
        else:
            return HttpResponse("No Entries in this feed yet")

def atom_feed(request, feedname=None):
    if feedname == None:
        return HttpResponse("Error")
    else:
        if Post.objects.count() > 0:
            fg = generateRSS("atom")
            return HttpResponse(fg.atom_str(pretty=True, encoding='UTF-8'), content_type='application/xml')
        else:
            return HttpResponse("No Entries in this feed yet")

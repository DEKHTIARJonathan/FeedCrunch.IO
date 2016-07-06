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
        posts = Post.objects.filter(user = feedname, activeLink=True).order_by('-id')
        user = FeedUser.objects.get(username=feedname)
        return render(request, 'index.html', {'posts': posts, 'user': user, 'rss_feed_display': True})


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
        if Post.objects.count() > 0:
            fg = generateRSS("rss", feedname)
            return HttpResponse(fg.rss_str(pretty=True, encoding='UTF-8'), content_type='application/xml')
        else:
            return HttpResponse("No Entries in this feed yet")

def atom_feed(request, feedname=None):
    if feedname == None:
        return HttpResponse("Error")
    else:
        if Post.objects.count() > 0:
            fg = generateRSS("atom", feedname)
            return HttpResponse(fg.atom_str(pretty=True, encoding='UTF-8'), content_type='application/xml')
        else:
            return HttpResponse("No Entries in this feed yet")

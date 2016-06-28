from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from feedcrunch.models import Post, FeedUser

from feedgen.feed import FeedGenerator
from .functions import *

# Create your views here.

def index(request, feedname=None):

    if feedname == None:
        return HttpResponse("Error, feedname = None")

    elif not FeedUser.objects.filter(username = feedname).select_related('User').exists():
        return HttpResponse("Error, feedname = " + feedname + " doesn't exist.")

    else:
        posts = Post.objects.all()
        return render(request, 'index.html', {'posts': posts})


def redirect(request, feedname=None, postID=None):
    if postID == None or feedname == None :
        return HttpResponse("Error")
    else:
        return HttpResponseRedirect("http://www.google.fr")

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

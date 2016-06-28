from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from feedradar.models import Post, FeedUser

from feedgen.feed import FeedGenerator
from .functions import *

# Create your views here.

def index(request, feedname=None):

    if feedname == None:
        return HttpResponse("Error, feedname = None")

    elif not FeedUser.objects.filter(username = feedname).exists():
        return HttpResponse("Error, feedname = " + feedname + " doesn't exist.")

    else:
        posts = Post.objects.filter(user=feedname)
        return render(request, 'index.html', {'posts': posts})


def redirect(request, feedname=None, postID=None):
    if postID == None or feedname == None :
        return HttpResponse("Error")

    elif not FeedUser.objects.filter(username = feedname).exists():
        return HttpResponse("Error, feedname = " + feedname + " doesn't exist.")

    elif not Post.objects.filter(user=feedname, id=postID).exists():
        return HttpResponse("Error, the requested post (id ="+ postID +") doesn't exist for the feed: "+ feedname)

    else:
        queried_post = Post.objects.get(user="dataradar", id=postID)
        return HttpResponseRedirect(queried_post.link)

def rss_feed(request, feedname=None):
    if feedname == None:
        return HttpResponse("Error")

    elif not FeedUser.objects.filter(username = feedname).exists():
        return HttpResponse("Error, feedname = " + feedname + " doesn't exist.")

    elif Post.objects.filter(user=feedname).count() > 0:
        fg = generateRSS(feedname, "rss")
        return HttpResponse(fg.rss_str(pretty=True, encoding='UTF-8'), content_type='application/xml')

    else:
        return HttpResponse("No Entries in this feed yet")

def atom_feed(request, feedname=None):
    if feedname == None:
        return HttpResponse("Error")
    else:
        if Post.objects.count() > 0:
            fg = generateRSS(feedname, "atom")
            return HttpResponse(fg.atom_str(pretty=True, encoding='UTF-8'), content_type='application/xml')
        else:
            return HttpResponse("No Entries in this feed yet")

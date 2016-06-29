from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import authenticate, login, logout

from feedcrunch.models import Post, FeedUser

import json

# Create your views here.

def index(request, feedname=None):

    context = RequestContext(request)
    if feedname == None:
        return HttpResponse("Error")

    elif not request.user.is_authenticated():
        return HttpResponse("Not logged in")

    elif feedname != request.user.username:
        return HttpResponseRedirect('/@'+request.user.username+'/admin')

    else:
        return render(request, 'admin_index.html')


def admin_add(request, feedname=None):
    context = RequestContext(request)
    if feedname == None:
        return HttpResponse("Error")

    elif not request.user.is_authenticated():
        return HttpResponse("Not logged in")

    elif feedname != request.user.username:
        return HttpResponseRedirect('/@'+request.user.username+'/admin')

    else:
        return render(request, 'admin_add.html')

def admin_add_ajax(request, feedname=None):
    context = RequestContext(request)
    if request.method == 'POST':

        if feedname == None:
            return HttpResponse("Error")

        elif (not request.user.is_authenticated()) or (not request.user.is_active):
            return HttpResponse("Not logged in or Account Not Activated")

        elif feedname != request.user.username:
            return HttpResponseRedirect('/@'+request.user.username+'/admin')

        else:
            title = request.POST['title']
            link = request.POST['link']
            if title == "" or link == "":
                return HttpResponse("Data Missing")
            else:
                tmp_user = FeedUser.objects.get(username=request.user.username)
                tmp_post = Post.objects.create(title=title, link=link, clicks=0, activeLink=True, user=tmp_user)
                tmp_post.save()
                return HttpResponse("1")

    else:
        return HttpResponse("Post Request Needed")

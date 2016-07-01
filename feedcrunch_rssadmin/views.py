# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import authenticate, login, logout

from feedcrunch.models import Post, FeedUser
from .tw_funcs import TwitterAPI
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
        return HttpResponseRedirect('/@'+request.user.username+'/admin')

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
        return render(request, 'admin_index.html')


def admin_add(request, feedname=None):

    check_passed = check_admin(feedname, request.user)
    if check_passed != True:
        return check_passed
    else:
        return render(request, 'admin_add.html')

def admin_add_ajax(request, feedname=None):

    if request.method == 'POST':

        check_passed = check_admin(feedname, request.user)
        if check_passed != True:
            return check_passed
        else:
            title = request.POST['title']
            link = request.POST['link']

            activated_bool = str2bool(request.POST['activated'])
            twitter_bool = str2bool(request.POST['twitter'])

            if str2bool(request.POST['autoformat']) :
                title = format_title(title)

            if title == "" or link == "":
                return HttpResponse("Data Missing")
            else:
                tmp_user = FeedUser.objects.get(username=request.user.username)

                tmp_post = Post.objects.create(title=title, link=link, clicks=0, user=tmp_user, activeLink=activated_bool)
                tmp_post.save()

                if twitter_bool and tmp_user.is_twitter_enabled():
                    twitter_instance = TwitterAPI(tmp_user)
                    twitter_instance.post_twitter(title, tmp_post.id)

                return HttpResponse("1")

    else:
        return HttpResponse("Post Request Needed")

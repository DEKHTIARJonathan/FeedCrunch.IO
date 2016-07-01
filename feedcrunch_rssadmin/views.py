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

def add_form(request, feedname=None):

    check_passed = check_admin(feedname, request.user)
    if check_passed != True:
        return check_passed
    else:
        return render(request, 'post_form.html')

def add_form_ajax(request, feedname=None):

    data = {}
    data["operation"] = "insert"

    if request.method == 'POST':

        check_passed = check_admin(feedname, request.user)
        if check_passed != True:
            return check_passed
        else:
            try:

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

                    data["status"] = "success"
                    data["postID"] = str(tmp_post.id)

            except:
                data["status"] = "error"
                data["error"] = "An error occured in the process"
                data["postID"] = str(postID)


    else:
        data["status"] = "error"
        data["error"] = "Only available with a POST Request"
        data["postID"] = str(postID)

    return JsonResponse(data)

def modify_form_ajax(request, feedname=None, postID=None):

    data = {}
    data["operation"] = "modification"

    if request.method == 'POST':

        check_passed = check_admin(feedname, request.user)
        if check_passed != True:
            return check_passed

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
                    return HttpResponse("Data Missing")

                post = Post.objects.get(id=postID, user=feedname)

                post.title = title
                post.link = link
                post.activeLink = activated_bool

                post.save()

                tmp_user = FeedUser.objects.get(username=request.user.username)
                if twitter_bool and tmp_user.is_twitter_enabled():
                    twitter_instance = TwitterAPI(tmp_user)
                    twitter_instance.post_twitter(title, tmp_post.id)

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

def delete_listing(request, feedname=None):

    check_passed = check_admin(feedname, request.user)
    if check_passed != True:
        return check_passed
    else:
        posts = Post.objects.filter(user = feedname).order_by('-id')
        return render(request, 'listing.html', {'posts': posts})

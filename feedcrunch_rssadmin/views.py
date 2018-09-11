#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime
import unicodedata
from calendar import monthrange

from django.core.validators import URLValidator
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse

from feedcrunch.models import Post
from feedcrunch.models import FeedUser
from feedcrunch.models import Country
from feedcrunch.models import RSSFeed_Sub
from feedcrunch.models import RSSArticle_Assoc
from feedcrunch.models import Interest
from feedcrunch.models import Option

from oauth.twitterAPI  import TwitterAPI
from oauth.facebookAPI import FacebookAPI
from oauth.linkedinAPI import LinkedInAPI
from oauth.slackAPI    import SlackAPI

from functions.check_admin import check_admin
from functions.custom_render import myrender as render


def index(request, feedname=None):

    check_passed = check_admin(feedname, request.user)

    if not check_passed:
        return check_passed

    else:
        d = datetime.datetime.now()
        monthtime_elapsed = int(round(float(d.day) / monthrange(d.year, d.month)[1] * 100,0))

        try:
            publication_trend = ((float(request.user.get_current_month_post_count()) / request.user.get_last_month_post_count()) -1 ) * 100.0

            if publication_trend > 0:
                post_trending = "trending_up"
                post_trending_color = "green-text"
            elif publication_trend < 0:
                post_trending = "trending_down"
                post_trending_color = "red-text"
            else :
                post_trending = "trending_flat"
                post_trending_color = "blue-grey-text"

            publication_trend = int(round(abs(publication_trend),0))

        except ZeroDivisionError:
            timedelta_registred = datetime.datetime.now() - request.user.date_joined.replace(tzinfo=None)
            if (timedelta_registred.days < 31):
                publication_trend = -1
                post_trending = "new_releases"
                post_trending_color = "blue-grey-text"
            else:
                publication_trend = 0
                post_trending = "trending_flat"
                post_trending_color = "blue-grey-text"

        data = {
            'monthtime_elapsed': monthtime_elapsed,
            'post_trending': post_trending,
            'publication_trend': publication_trend,
            'post_trending_color': post_trending_color,
        }

        return render(request, 'admin/admin_dashboard.html', data)


def personal_info_form(request, feedname=None):

    check_passed = check_admin(feedname, request.user)
    if not check_passed:
        return check_passed

    else:

        country_list = Country.objects.all().order_by('name')
        return render(request, 'admin/admin_personal.html', {'countries': country_list})


def preferences_form(request, feedname=None):

    check_passed = check_admin(feedname, request.user)
    if not check_passed:
        return check_passed
    else:
        return render(request, 'admin/admin_preferences.html', {"social_networks_enabled": request.user.is_social_network_enabled()})


def password_form(request, feedname=None):

    check_passed = check_admin(feedname, request.user)
    if not check_passed:
        return check_passed
    else:
        return render(request, 'admin/admin_password.html')


def picture_form(request, feedname=None):

    check_passed = check_admin(feedname, request.user)
    if not check_passed:
        return check_passed
    else:
        return render(request, 'admin/admin_photo.html')


def social_form(request, feedname=None):

    check_passed = check_admin(feedname, request.user)
    if not check_passed:
        return check_passed
    else:
        return render(request, 'admin/admin_social_accounts.html')


def slack_management(request, feedname=None):

    check_passed = check_admin(feedname, request.user)
    if not check_passed:
        return check_passed
    else:
        request_data = dict()

        slack_teams = dict()

        for team in request.user.rel_slack_integrations.all():
             api_response = SlackAPI(team).get_available_channels()

             if api_response["status"]:
                 slack_teams[team.team_name] = api_response["channels"]

        request_data["teams"] = slack_teams
        request_data["slack_auth_url"] = SlackAPI.get_authorization_url()

        return render(request, 'admin/admin_slack_management.html', request_data)


def services_form(request, feedname=None):

    check_passed = check_admin(feedname, request.user)
    if not check_passed:
        return check_passed
    else:
        request_data = dict()

        if not request.user.is_social_network_activated(network="twitter"):
            request_data["twitter_auth_url"] = TwitterAPI.get_authorization_url(request)
        else:
            request_data["twitter_auth_url"] = False # False => Don't need to authenticate with Twitter

        if not request.user.is_social_network_activated(network="facebook"):
            request_data["facebook_auth_url"] = FacebookAPI.get_authorization_url()
        else:
            request_data["facebook_auth_url"] = False # False => Don't need to authenticate with Facebook

        if not request.user.is_social_network_activated(network="linkedin"):
            request_data["linkedin_auth_url"] = LinkedInAPI.get_authorization_url()
        else:
            request_data["linkedin_auth_url"] = False # False => Don't need to authenticate with LinkedIn

        request_data["slack_auth_url"] = SlackAPI.get_authorization_url()

        return render(request, 'admin/admin_social_sharing.html', request_data)


def add_article_form(request, feedname=None):

    check_passed = check_admin(feedname, request.user)
    if not check_passed:
        return check_passed
    else:
        return render(request, 'admin/admin_article_form.html')


def modify_article_form(request, feedname=None, postID=None):

    check_passed = check_admin(feedname, request.user)
    if not check_passed:
        return check_passed

    elif postID == None:
        return HttpResponseRedirect("/@"+feedname+"/admin/modify")

    else:
        try:
            post = Post.objects.get(id=postID, user=feedname)
            return render(request, 'admin/admin_article_form.html', {"post": post})

        except:
            return HttpResponseRedirect("/@"+feedname+"/admin/modify")


def modify_article_listing(request, feedname=None):

    check_passed = check_admin(feedname, request.user)
    if not check_passed:
        return check_passed
    else:
        posts = Post.objects.filter(user = feedname).order_by('-id')
        return render(request, 'admin/admin_post_listing.html', {'posts': posts})


def delete_article_listing(request, feedname=None):

    check_passed = check_admin(feedname, request.user)
    if not check_passed:
        return check_passed
    else:
        posts = Post.objects.filter(user = feedname).order_by('-id')
        return render(request, 'admin/admin_post_listing.html', {'posts': posts})


def contact_form(request, feedname=None):

    check_passed = check_admin(feedname, request.user)
    if not check_passed:
        return check_passed
    else:
        return render(request, 'admin/admin_contact.html')


def upload_picture(request, feedname=None):
    try:

        if request.method == 'POST':

            if check_admin(feedname, request.user) != True:
                raise Exception("You are not allowed to perform this action")

            else:
                photo = request.FILES['photo']

                allowed_mime_types = ['image/gif', 'image/jpeg', 'image/pjpeg', 'image/png']

                if photo.content_type not in allowed_mime_types:
                    raise ValueError("Only Images are allowed.")


                """
                # Not functioning at the time
                w, h = get_image_dimensions(photo.read())
                if not(isinstance(w, int) and isinstance(h, int) and w > 0 and h > 0):
                    raise ValueError("Picture dimensions are not correct.")

                """
                if photo.size > 1048576: # > 1MB
                    raise ValueError("File size is larger than 1MB.")

                else:
                    tmp_user = FeedUser.objects.get(username=request.user.username)
                    tmp_user.profile_picture = photo
                    tmp_user.save()

        else:
            raise Exception("Only POST Requests Allowed.")

    except Exception as e:
        data = dict()
        data["status"] = "error"
        data["error"] = "An error occured in the process: " + str(e)
        data["feedname"] = feedname
        return JsonResponse(data)

    return HttpResponseRedirect('/@'+request.user.username+'/admin/account/picture/')


def sub_management(request, feedname=None):
    check_passed = check_admin(feedname, request.user)
    if not check_passed:
        return check_passed
    else:
        feeds = RSSFeed_Sub.objects.filter(user=feedname, feed__active=True).order_by("title")
        return render(request, 'admin/admin_sub_listing.html', {'feeds': feeds})


def reading_recommendation(request, feedname=None):
    check_passed = check_admin(feedname, request.user)
    if not check_passed:
        return check_passed
    else:

        ###################### Getting the Option Value for the amount of old articles retrieved by RSS Feed ##############################
        try:
            max_recommendations = int(Option.objects.get(parameter="max_recommendations").value)
            recommendation_decay = float(60) / max_recommendations

        except ObjectDoesNotExist:
            raise Exception("The Option 'max_recommendations' is not defined")

        #rssarticles = RSSArticle_Assoc.objects.filter(rel_sub_article_assoc__user=request.user, rel_sub_article_assoc__marked_read = False).order_by('-added_date')
        rssarticles = RSSArticle_Assoc.objects.filter(user=request.user, marked_read = False).order_by('-article__added_date')[:max_recommendations]

        rssarticles_data = []

        for i, article in enumerate(rssarticles):
            recommendation_score = 97.3 - recommendation_decay*i
            tmp = {
                'id': article.id,
                'short_title': article.short_title(),
                'title': article.title(),
                'rssfeed': article.short_rssfeed(),
                'get_domain': article.short_domain(),
                'link': article.link(),
                'score': recommendation_score,
                'color': int(2.55*recommendation_score),
                'get_shortdate': article.get_shortdate(),
            }

            rssarticles_data.append(tmp)

        print (len(rssarticles_data))
        return render(request, 'admin/admin_reading_recommendation.html', {'rssarticles': rssarticles_data})


def redirect_recommendation(request, feedname=None, RSSArticle_AssocID=None):
    check_passed = check_admin(feedname, request.user)
    if not check_passed:
        return check_passed

    try:
        tmp_article = RSSArticle_Assoc.objects.get(id=RSSArticle_AssocID, user=feedname)

        tmp_article.open_count += 1
        tmp_article.save()

        return HttpResponseRedirect(tmp_article.article.link)
    except:
        return HttpResponseRedirect("/@"+feedname+"/admin/reading/recommendation/")


def onboarding_view(request, feedname=None):

    check_passed = check_admin(feedname, request.user, bypassOnboardingCheck = True)
    if not check_passed:
        return check_passed

    else:
        interest_list = Interest.objects.all().order_by('name')
        country_list = Country.objects.all().order_by('name')

        request_data = dict()

        if not request.user.is_social_network_activated(network="twitter"):
            request_data["twitter_auth_url"] = TwitterAPI.get_authorization_url(request)
        else:
            request_data["twitter_auth_url"] = False # False => Don't need to authenticate with Twitter

        if not request.user.is_social_network_activated(network="facebook"):
            request_data["facebook_auth_url"] = FacebookAPI.get_authorization_url()
        else:
            request_data["facebook_auth_url"] = False # False => Don't need to authenticate with Facebook

        if not request.user.is_social_network_activated(network="linkedin"):
            request_data["linkedin_auth_url"] = LinkedInAPI.get_authorization_url()
        else:
            request_data["linkedin_auth_url"] = False # False => Don't need to authenticate with LinkedIn

        request_data["slack_auth_url"] = SlackAPI.get_authorization_url()

        request_data['interests'] = interest_list
        request_data['countries'] = country_list

        return render(request, 'admin/onboarding.html', request_data)


def process_onboarding_view(request, feedname=None):

    check_passed = check_admin(feedname, request.user, bypassOnboardingCheck = True)
    if not check_passed:
        return check_passed

    else:
        payload = dict()

        payload["success"] = True
        payload["feedname"] = request.user.username

        val = URLValidator()

        fields = [
            'firstname',
            'lastname',
            'email',
            'birthdate',
            'country',
            'gender',
            'feedtitle', # not Checked
            'description', # not Checked
            'job', # not Checked
            'company_name', # not Checked
            'company_website'
        ]

        form_data = dict()
        for field in fields:
            form_data[field] = unicodedata.normalize('NFC', request.POST[field])

        FeedUser.objects._validate_firstname(form_data["firstname"])
        FeedUser.objects._validate_lastname(form_data["lastname"])
        FeedUser.objects._validate_email(form_data["email"])
        FeedUser.objects._validate_birthdate(form_data["birthdate"])

        FeedUser.objects._validate_country(form_data["country"])
        FeedUser.objects._validate_gender(form_data["gender"])

        val(form_data["company_website"])

        request.user.first_name = form_data["firstname"]
        request.user.last_name = form_data["lastname"]
        request.user.email = form_data["email"]
        request.user.birthdate = datetime.datetime.strptime(form_data["birthdate"], '%d/%m/%Y').date()
        request.user.country = Country.objects.get(name=form_data["country"])
        request.user.gender = form_data["gender"]
        request.user.rss_feed_title = form_data["feedtitle"]
        request.user.description = form_data["description"]
        request.user.job = form_data["job"]
        request.user.company_name = form_data["company_name"]
        request.user.company_website = form_data["company_website"]


        interest_fields = [
            'interest1',
            'interest2',
            'interest3',
        ]

        request.user.interests.clear()

        ###################### Getting the Option Value for the amount of old articles retrieved by RSS Feed ##############################
        try:
            max_old_articles_retrieved_on_interest = int(Option.objects.get(parameter="max_articles_on_interest_sub").value)
        except ObjectDoesNotExist:
            raise Exception("The Option 'max_articles_on_interest_sub' is not defined")

        ###################### LOOPING THROUGH INTERESTS AND ADD THEM TO THE USER ##############################
        for interest in interest_fields:
            tmp_interest = Interest.objects.get(name=unicodedata.normalize('NFC', request.POST[interest]))
            request.user.interests.add(tmp_interest)

            ##### ================== Subcribe the user to the feeds linked to the interest ============================== ####
            for feed in tmp_interest.rssfeeds.all():
                # ======= Subscribe User to RSS Feed ======== #

                try:
                    # We subscribe the use to the feed.
                    tmp_sub = RSSFeed_Sub.objects.create(user= request.user, feed=feed, title=feed.title)

                    # We get the N last articles articles published in the feed and loop through them:
                    for article in feed.rel_rss_feed_articles.all().order_by("-added_date")[:max_old_articles_retrieved_on_interest] :
                        RSSArticle_Assoc.objects.create(subscription=tmp_sub, user=request.user, article=article)

                except: #If already subscribed, keep going to the next feed.
                    continue

        request.user.onboarding_done = True
        request.user.save()

        return HttpResponseRedirect(reverse(index, kwargs={'feedname': request.user.username}))

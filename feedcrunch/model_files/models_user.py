#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import re
import uuid
import datetime
import unicodedata
import random
import urllib
import string

from xml.sax.saxutils import escape as escape_xml

from django.conf import settings

from django.contrib.auth.models import UserManager
from django.contrib.auth.models import PermissionsMixin

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser

from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from django.db import models

from django.utils import six
from django.utils import timezone
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from pyisemail import is_email
from encrypted_model_fields.fields import EncryptedCharField

from feedcrunch.models import Country
from feedcrunch.models import Estimator
from feedcrunch.models import Interest

from oauth.twitterAPI  import TwitterAPI
from oauth.facebookAPI import FacebookAPI
from oauth.linkedinAPI import LinkedInAPI
from oauth.slackAPI    import SlackAPI

from functions.validators import UnicodeUsernameValidator
from functions.validators import ASCIIUsernameValidator

from datetime import timedelta
from datetime import datetime


def generateDummyDesc():
    return "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam dui nisl, aliquam nec quam nec, laoreet porta odio. Morbi ultrices sagittis ligula ut consectetur. Aenean quis facilisis augue. Vestibulum maximus aliquam augue, ut lobortis turpis euismod vel. Sed in mollis tellus, eget eleifend turpis. Vivamus aliquam ornare felis at dignissim. Integer vitae cursus eros, non dignissim dui. Suspendisse porttitor justo nec lacus dictum commodo. Sed in fringilla tortor, at pharetra tortor."


def id_generator(size=20, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_photo_path(instance, filename):
    ext = filename.split('.')[-1]

    while True:
        filename = "%s.%s" % (id_generator(), ext)

        photo_url = "%s%s" % (settings.MEDIA_URL, filename)

        if settings.DEBUG or urllib.urlopen(photo_url).getcode() != 200:
            break

    return settings.USER_PHOTO_PATH + filename


class FeedUserManager(BaseUserManager):

        use_in_migrations = True

        def _validate_username(self, username):
            if (not isinstance( username, str )) or len( username ) >= 31:
                raise ValueError("The given username is not a valid string or longer than 30 characters.")

            if not re.match("^[A-Za-z0-9]*$", username):
                raise ValueError("The given username is not a valid string, it should only contains letters (A-Z and a-z) and numbers (0-9)")

            if FeedUser.objects.filter(username=username).exists():
                raise ValueError("The given username `%s` is already taken" % username)

        def _validate_email(self, email):
            if not is_email(email, check_dns=True):
                raise ValueError("The given email `%s` is not valid or not does not exist." % email)

        def _validate_password(self, password):
            if re.match("(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}", password) == None:
                raise ValueError("The password doesn't fit in our policies : At least 8 characters, 1 Uppercase letter 'A-Z', 1 Lowercase letter 'a-z', and 1 number '0-9'")

        def _validate_firstname(self, firstname):
            if (not isinstance( firstname, str )) or len( firstname ) >= 31:
                raise ValueError("The given firstname is not a valid string or longer than 30 characters.")

        def _validate_lastname(self, lastname):
            if (not isinstance( lastname, str )) or len( lastname ) >= 31:
                raise ValueError("The given last_name is not a valid string or longer than 30 characters.")

        def _validate_country(self, country):
            if not Country.objects.filter(name = country).exists():
                raise ValueError("The given country ( "+ country +" ) doesn't exist")

        def _validate_gender(self, gender):
            if gender not in ['M', 'F']:
                raise ValueError("The given gender value is not valid : 'M' or 'F'.")

        def _validate_birthdate(self, birthdate):

            today = datetime.now().date()

            if datetime.strptime(birthdate, '%d/%m/%Y').date() > today:
                raise ValueError("The given birthdate can't be in the future. Please provide a correct date.")

        def _validate_parameters(self, username, email, password):

            try:
                self._validate_username(username)
                self._validate_email(email)
                self._validate_password(password)

                return {'status': True}

            except Exception as e:
                return {'status': False, 'error': str(e)}

        def _normalize_username(self, username):
            return unicodedata.normalize('NFKC', force_text(username).lower())

        def _create_user(self, username, email, password, **extra_fields):
                """
                Creates and saves a User with the given username, email and password.
                """

                is_staff     = extra_fields.get('is_staff')
                is_superuser = extra_fields.get('is_superuser')

                username     = self._normalize_username(username)
                email        = self.normalize_email(email)

                validation = self._validate_parameters(username, email, password)

                if validation['status']:

                    if 'firstname' in extra_fields:
                        firstname = extra_fields.get('firstname')
                        self._validate_firstname(firstname)
                    else:
                        firstname = ""

                    if 'lastname' in extra_fields:
                        lastname = extra_fields.get('lastname')
                        self._validate_lastname(lastname)
                    else:
                        lastname = ""

                    if 'country' in extra_fields:
                        country = extra_fields.get('country')
                        self._validate_country(country)
                        country = Country.objects.get(name=country)
                    else:
                        country = None

                    if 'gender' in extra_fields:
                        gender = extra_fields.get('gender')
                        self._validate_gender(gender)
                    else:
                        gender = None

                    if 'birthdate' in extra_fields:
                        birthdate = extra_fields.get('birthdate')
                        self._validate_birthdate(birthdate)
                        birthdate = datetime.strptime(birthdate, '%d/%m/%Y').date()
                    else:
                        birthdate = None

                    user = self.model(
                        username=username,
                        email=email,
                        password="###", #Temporary value replaced below
                        first_name=firstname,
                        last_name=lastname,
                        country=country,
                        gender=gender,
                        birthdate = birthdate,
                        is_staff = is_staff,
                        is_superuser = is_superuser
                    )
                    user.set_password(password)
                    user.save(using=self._db)

                    from feedcrunch.tasks import send_welcome_email
                    send_welcome_email.delay(username=user.username)

                    return user

                else:
                    raise Exception(validation['error'])

        def create_user(self, username, email, password, **extra_fields):
                extra_fields.setdefault('is_staff', False)
                extra_fields.setdefault('is_superuser', False)

                return self._create_user(username, email, password, **extra_fields)

        def create_superuser(self, username, email, password, **extra_fields):
                extra_fields.setdefault('is_staff', True)
                extra_fields.setdefault('is_superuser', True)

                if extra_fields.get('is_staff') is not True:
                        raise ValueError('Superuser must have is_staff=True.')
                if extra_fields.get('is_superuser') is not True:
                        raise ValueError('Superuser must have is_superuser=True.')

                return self._create_user(username, email, password, **extra_fields)


class AbstractFeedUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    Username and password are required. Other fields are optional.
    """
    username_validator = UnicodeUsernameValidator() if six.PY3 else ASCIIUsernameValidator()

    username    = models.CharField(
        _('username'),
        max_length=150,
        primary_key=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name  = models.CharField(_('first name'), max_length=30, default='', blank=True, null=True )
    last_name   = models.CharField(_('last name'), max_length=30, default='', blank=True, null=True )
    email       = models.EmailField(
        _('email address'),
        unique=True,
        help_text=_('Required. 255 characters or fewer and a valid email.'),
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    is_staff    = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active   = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def clean(self):
        super(AbstractBaseUser, self).clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_full_name_formatted(self):
        """
        Returns the first_name in title format plus the last_name in capital case, with a space in between.
        """
        full_name = '%s %s' % (self.first_name.title(), self.last_name.upper())
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class FeedUser(AbstractFeedUser):

    ################################### ============================== ###################################
    #                                        GENERAL Information                                         #
    ################################### ============================== ###################################

    country     = models.ForeignKey(Country, on_delete=models.CASCADE, default=None, blank=True, null=True )
    birthdate   = models.DateField(default=None, blank=True, null=True )
    description = models.TextField(default=generateDummyDesc(), blank=True, null=True)

    gender      = models.CharField(
        max_length=1,
        choices=(('F', 'Female'),('M', 'Male'),('O', 'Other')),
        default=None,
        blank=True,
        null=True
    )

    rss_feed_title  = models.CharField(max_length=100, default='', blank=True, null=True)

    job             = models.CharField(max_length=80, default='Chief Admission Officer at', blank=True, null=True)
    company_name    = models.CharField(max_length=80, default='Holy Paradise Inc.', blank=True, null=True)
    company_website = models.URLField(max_length=120, default='https://www.feedcrunch.io/', blank=True, null=True)

    profile_picture = models.ImageField(upload_to=get_photo_path, default=settings.USER_PHOTO_PATH+'dummy_user.png', blank=True, null=True)
    onboarding_done = models.BooleanField(default=False)

    ################################### ============================== ###################################
    #                                           API KEY ACCESS                                           #
    ################################### ============================== ###################################

    apikey = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=False)

    ################################### ============================== ###################################
    #                                           RECOMMENDATION                                           #
    ################################### ============================== ###################################

    interests = models.ManyToManyField(Interest, related_name="users_by_interest", blank=True)
    recommendation_engine = models.OneToOneField(Estimator, on_delete=models.CASCADE, default=None, blank=True, null=True)

    ################################### ============================== ###################################
    #                                            SOCIAL TOKENS                                           #
    ################################### ============================== ###################################

    twitter_token                  = EncryptedCharField(max_length=500, default='', blank=True, null=True)
    twitter_token_secret           = EncryptedCharField(max_length=500, default='', blank=True, null=True)

    facebook_access_token          = EncryptedCharField(max_length=500, default='', blank=True, null=True)
    facebook_token_expire_datetime = models.DateTimeField(auto_now_add=False, default=None, blank=True, null=True)

    linkedin_access_token          = EncryptedCharField(max_length=500, default='', blank=True, null=True)
    linkedin_token_expire_datetime = models.DateTimeField(auto_now_add=False, default=None, blank=True, null=True)

    social_fields = {
        'twitter' : {
            'token'           : "twitter_token",
            'secret'          : "twitter_token_secret"
        },
        'facebook' : {
            'token'           : "facebook_access_token",
            'expire_datetime' : "facebook_token_expire_datetime"
        },
        'linkedin' : {
            'token'           : "linkedin_access_token",
            'expire_datetime' : "linkedin_token_expire_datetime"
        },
    }

    ################################### ============================== ###################################
    #                                          USER PREFERENCES                                          #
    ################################### ============================== ###################################

    pref_post_public_visibility   = models.BooleanField(default=True)
    pref_post_autoformat          = models.BooleanField(default=False)

    # ======================== Social Repost ========================

    pref_post_repost_TW           = models.BooleanField(default=False)
    pref_post_repost_FB           = models.BooleanField(default=False)
    pref_post_repost_LKin         = models.BooleanField(default=False)
    pref_post_repost_Slack        = models.BooleanField(default=False)

    ################################### ============================== ###################################
    #                                       NEWSLETTER PREFERENCES                                       #
    ################################### ============================== ###################################

    pref_newsletter_subscription  = models.BooleanField(default=True)

    ################################### ============================== ###################################
    #                                            SOCIAL LINKS                                            #
    ################################### ============================== ###################################

    # Main Social Networks
    social_dribbble         = models.URLField(max_length=60, default='', blank=True, null=True)
    social_facebook         = models.URLField(max_length=60, default='', blank=True, null=True)
    social_flickr           = models.URLField(max_length=60, default='', blank=True, null=True)
    social_gplus            = models.URLField(max_length=60, default='', blank=True, null=True)
    social_instagram        = models.URLField(max_length=60, default='', blank=True, null=True)
    social_linkedin         = models.URLField(max_length=60, default='', blank=True, null=True)
    social_pinterest        = models.URLField(max_length=60, default='', blank=True, null=True)
    social_stumble          = models.URLField(max_length=60, default='', blank=True, null=True)
    social_twitter          = models.URLField(max_length=60, default='', blank=True, null=True)
    social_vimeo            = models.URLField(max_length=60, default='', blank=True, null=True)
    social_youtube          = models.URLField(max_length=60, default='', blank=True, null=True)

    # Computer Science Networks
    social_docker           = models.URLField(max_length=60, default='', blank=True, null=True)
    social_git              = models.URLField(max_length=60, default='', blank=True, null=True)
    social_kaggle           = models.URLField(max_length=60, default='', blank=True, null=True)
    social_stackoverflow    = models.URLField(max_length=60, default='', blank=True, null=True)

    # MooC Profiles
    social_coursera         = models.URLField(max_length=60, default='', blank=True, null=True)

    # Research Social Networks
    social_google_scholar   = models.URLField(max_length=60, default='', blank=True, null=True)
    social_orcid            = models.URLField(max_length=60, default='', blank=True, null=True)
    social_researchgate     = models.URLField(max_length=60, default='', blank=True, null=True)
    social_mendeley         = models.URLField(max_length=60, default='', blank=True, null=True)

    # Personal Webpage & Blog
    social_blog             = models.URLField(max_length=60, default='', blank=True, null=True)
    social_personalwebsite  = models.URLField(max_length=60, default='', blank=True, null=True)

    ################################### ============================== ###################################
    #                                           MISC Properties                                          #
    ################################### ============================== ###################################

    objects = FeedUserManager()

    class Meta(AbstractFeedUser.Meta):
            swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.interests.count() > 3:
            raise ValidationError("You can't assign more than three interests")

        super(FeedUser, self).save(*args, **kwargs) # Call the "real" save() method.

    # ====================================================================================================
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    ################################### ============================== ###################################
    #                                            USER METHODS                                            #
    ################################### ============================== ###################################
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # ====================================================================================================

    ################################### ============================== ###################################
    #                                         User Data Accessors                                        #
    ################################### ============================== ###################################

    def get_birthdate_as_string(self):
        if self.birthdate is not None:
            return self.birthdate.strftime("%d/%m/%Y")
        else:
            return

    def get_profile_picture_url(self):
        if settings.DEBUG or settings.TESTING:
            return self.profile_picture.url
        else:
            photo_url = "%s%s" % (settings.MEDIA_URL, self.profile_picture)
            return photo_url

    ################################### ============================== ###################################
    #                                       User Publication Stats                                       #
    ################################### ============================== ###################################
    def get_post_count(self):
        return self.rel_posts.count()

    def get_clicks_count_on_user_posts(self):
        return self.rel_posts.all().aggregate(models.Sum('clicks'))['clicks__sum']

    def get_current_month_post_count(self):
        date_1st_day_month = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0, day=1)

        return self.rel_posts.filter(when__gte=date_1st_day_month).count()

    def get_last_month_post_count(self):

        date_last_day_last_month = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0, day=1) - timedelta(days=1)

        date_1st_day_last_month = date_last_day_last_month.replace(day=1)

        return self.rel_posts.filter(when__lte=date_last_day_last_month, when__gte=date_1st_day_last_month).count()

    ################################### ============================== ###################################
    #                                       User subscription Stats                                      #
    ################################### ============================== ###################################

    def get_rss_subscription_count(self):
        return self.rel_sub_feed.count()

    ################################### ============================== ###################################
    #                                       User Subscribers Stats                                      #
    ################################### ============================== ###################################

    def get_user_subscribers_count(self, days_offset=1):

        today           = datetime.now().date()
        lookup_day      = today - timedelta(days=days_offset)

        subscribers_queryset = self.rel_rss_subscribers_count.filter(user=self, date=lookup_day).order_by('-date')

        if subscribers_queryset.count() == 0 :
            return 0
        else:
            return subscribers_queryset[0].count

    ################################### ============================== ###################################
    #                                         Social Net. Methods                                        #
    ################################### ============================== ###################################

    def is_social_network_enabled(self, network=None):
        if network is None:

            rslt = dict()

            for social_net in list(self.social_fields.keys()) + ["slack"]:
                rslt[social_net] = self.is_social_network_enabled(network=social_net)

            return rslt

        if network in ["facebook", "linkedin"]:
            token           = getattr(self, self.social_fields[network]["token"])
            expire_datetime = getattr(self, self.social_fields[network]["expire_datetime"])

            if expire_datetime is not None:
                return token != "" and datetime.now() < expire_datetime.replace(tzinfo=None)
            else:
                return  False

        elif network == "twitter":
            token  = getattr(self, self.social_fields[network]["token"])
            secret = getattr(self, self.social_fields[network]["secret"])
            return token != "" and secret != ""

        elif network == "slack":
            return bool(self.rel_slack_integrations.all().count())

        else:
            raise Exception("The network requested " + network + " doesn't exist in this application")


    def is_twitter_enabled(self):
        return self.is_social_network_enabled(network="twitter")

    def is_facebook_enabled(self):
        return self.is_social_network_enabled(network="facebook")

    def is_linkedin_enabled(self):
        return self.is_social_network_enabled(network="linkedin")

    def is_slack_enabled(self):
        return self.is_social_network_enabled(network="slack")

    def is_social_network_activated(self, network):
        if network == "twitter":
            if self.is_social_network_enabled(network=network):
                if TwitterAPI(self).verify_credentials()['status']:
                    return True
                else:
                    self.reset_social_network_credentials(network=network)
                    return False
            else:
                return False

        elif network == "facebook":
            if self.is_social_network_enabled(network=network):
                if FacebookAPI(self).verify_credentials()['status']:
                    return True
                else:
                    self.reset_social_network_credentials(network=network)
                    return False
            else:
                return False

        elif network == "linkedin":
            if self.is_social_network_enabled(network=network):
                if LinkedInAPI(self).verify_credentials()['status']:
                    return True
                else:
                    self.reset_social_network_credentials(network=network)
                    return False
            else:
                return False

        elif network == "slack":
            if self.is_social_network_enabled(network=network):
                if SlackAPI(self).verify_credentials()['status']:
                    return True
                else:
                    self.reset_social_network_credentials(network=network)
                    return False
            else:
                return False

        else:
            raise Exception("The network requested " + network + " doesn't exist in this application")

    def reset_social_network_credentials(self, network):
        if network in ["facebook", "linkedin"]:
            setattr(self, self.social_fields[network]["token"], "")
            setattr(self, self.social_fields[network]["expire_datetime"], None)

        elif network == "twitter":
            setattr(self, self.social_fields[network]["token"], "")
            setattr(self, self.social_fields[network]["secret"], "")

        elif network == "slack":
            self.rel_slack_integrations.all().delete()
        else:
            raise Exception("The network requested " + network + " doesn't exist in this application")

        self.save()
    ################################### ============================== ###################################
    #                                       subscription Management                                      #
    ################################### ============================== ###################################

    def export_opml(self):

        OPML_START = """<?xml version="1.0" encoding="UTF-8"?>
            <!-- OPML generated by FeedCrunch.io -->
            <opml version="1.1">
                <head>
                    <title>User = """ + self.username +""" - FeedCrunch Feeds Export</title>
                </head>
                <body>
        """

        BODY = ""

        for subscription in self.rel_sub_feed.all():
            sub_link = subscription.link()
            sub_title = escape_xml(subscription.title)
            BODY += '<outline type="rss" xmlUrl="'+sub_link+'" htmlUrl="'+sub_link+'" title="'+sub_title+'"/>'
            BODY += '\n'

        OPML_END = """</body>
            </opml>
        """
        #opml = re.sub('\s+',' ', OPML_START + OPML_END)
        opml = OPML_START + BODY + OPML_END
        return opml.replace("\t", "")

    def load_opml(self, opml_file):
        from feedcrunch.models import RSSFeed, RSSArticle_Assoc, RSSFeed_Sub
        import untangle

        obj = untangle.parse(opml_file)

        errors = []
        for feed in obj.opml.body.outline:

            if feed["title"] != "" and feed["title"] is not None:
                title = feed["title"]
            elif feed["text"] != "" and feed["text"] is not None:
                title = feed["text"]
            else:
                continue

            if feed["xmlUrl"] != "" and feed["xmlUrl"] is not None:
                link = feed["xmlUrl"]
            elif feed["htmlUrl"] != "" and feed["htmlUrl"] is not None:
                link = feed["htmlUrl"]
            else:
                continue # Go to next Feed

            rssfeed_queryset = RSSFeed.objects.filter(link=link)

            if not rssfeed_queryset.exists():
                try:
                    tmp_rssfeed = RSSFeed.objects.create(title=title, link=link)
                except:
                    errors.append(link)
                    continue

                from feedcrunch.tasks import check_rss_feed
                check_rss_feed.delay(rss_id=tmp_rssfeed.id)

                old_articles = None

            else:
                tmp_rssfeed = rssfeed_queryset[0]
                old_articles = RSSArticle_Assoc.objects.filter(article__rssfeed=tmp_rssfeed)

            try:
                tmp_sub = RSSFeed_Sub.objects.create(user= self, feed=tmp_rssfeed, title=title)

                if ((old_articles is not None) and (old_articles.count() > 0 )):
                    for article in old_articles:
                        article.subscription = tmp_sub
                        article.save()
            except:
                continue

        return errors

    def refresh_user_subscriptions(self):

        for feed_assoc in self.rel_sub_feed.all():
            feed = feed_assoc.feed
            if feed.active:
                from feedcrunch.tasks import check_rss_feed
                check_rss_feed.delay(rss_id=feed.id)

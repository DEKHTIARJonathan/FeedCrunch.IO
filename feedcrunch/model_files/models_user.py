#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
######### https://github.com/django/django/blob/master/django/contrib/auth/models.py

import os, re, uuid, datetime, unicodedata, getenv, random, urllib, string

from django.conf import settings
from django.contrib.auth.models import User, UserManager, PermissionsMixin, AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import six, timezone
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from django_q.tasks import schedule
from django_q.models import Schedule

from validate_email import validate_email
from encrypted_fields import EncryptedCharField

from feedcrunch.models import Continent, Country, Estimator
from twitter.tw_funcs import *

from twython import Twython

from validators import ASCIIUsernameValidator, UnicodeUsernameValidator

def generateDummyDesc():
	return "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam dui nisl, aliquam nec quam nec, laoreet porta odio. Morbi ultrices sagittis ligula ut consectetur. Aenean quis facilisis augue. Vestibulum maximus aliquam augue, ut lobortis turpis euismod vel. Sed in mollis tellus, eget eleifend turpis. Vivamus aliquam ornare felis at dignissim. Integer vitae cursus eros, non dignissim dui. Suspendisse porttitor justo nec lacus dictum commodo. Sed in fringilla tortor, at pharetra tortor. Vestibulum tempor sapien id justo molestie imperdiet. Nulla efficitur mattis ante, nec iaculis lorem consequat in. Nullam sit amet diam augue. Nulla ullamcorper imperdiet turpis a maximus. Donec iaculis porttitor ultrices. Morbi lobortis dui molestie ullamcorper varius. Maecenas eu laoreet ipsum orci aliquam."

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
			if (not isinstance( username, unicode )) or len( username ) >= 31:
				raise ValueError("The given username is not a valid string or longer than 30 characters.")

			if not re.match("^[A-Za-z0-9]*$", username):
				raise ValueError("The given username is not a valid string, it should only contains letters (A-Z and a-z) and numbers (0-9)")

			if FeedUser.objects.filter(username = username).exists():
				raise ValueError("The given username ( "+ username +" ) is already taken")

		def _validate_email(self, email):
			if not validate_email(email):
				raise ValueError("The given email is not valid or not doesn''t exist.")

		def _validate_password(self, password):
			if re.match(r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[a-zA-Z\d]{8,}', password) == None:
				raise ValueError("The password doesn't fit in our policies : At least 8 characters, 1 Uppercase letter 'A-Z', 1 Lowercase letter 'a-z', and 1 number '0-9'")

		def _validate_firstname(self, firstname):
			if (not isinstance( firstname, unicode )) or len( firstname ) >= 31:
				raise ValueError("The given firstname is not a valid string or longer than 30 characters.")

		def _validate_lastname(self, lastname):
			if (not isinstance( lastname, unicode )) or len( lastname ) >= 31:
				raise ValueError("The given last_name is not a valid string or longer than 30 characters.")

		def _validate_country(self, country):
			if not Country.objects.filter(name = country).exists():
				raise ValueError("The given country ( "+ country +" ) doesn't exist")

		def _validate_gender(self, gender):
			if gender not in ['M', 'F']:
				raise ValueError("The given gender value is not valid : 'M' or 'F'.")

		def _validate_birthdate(self, birthdate):

			today = datetime.date.today()

			if datetime.datetime.strptime(birthdate, '%d/%m/%Y').date() > today:
				raise ValueError("The given birthdate can't be in the future. Please provide a correct date.")

		def _validate_parameters(self, username, email, password):

			try:
				self._validate_username(username)
				self._validate_email(email)
				self._validate_password(password)

				return {'status': True}

			except Exception, e:
				return {'status': False, 'error': str(e)}

		def _normalize_username(self, username):
			return unicodedata.normalize('NFKC', force_text(username).lower())

		def _create_user(self, username, email, password, **extra_fields):
				"""
				Creates and saves a User with the given username, email and password.
				"""

				is_staff = extra_fields.get('is_staff')
				is_superuser = extra_fields.get('is_superuser')

				username = self._normalize_username(username)
				email = self.normalize_email(email)

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
						birthdate = datetime.datetime.strptime(birthdate, '%d/%m/%Y').date()
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

					schedule('feedcrunch.tasks.send_welcome_email', user_name=user.username, schedule_type=Schedule.ONCE, next_run=timezone.now() + datetime.timedelta(minutes=1))

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

	username = models.CharField(
		_('username'),
		max_length=150,
		primary_key=True,
		help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
		validators=[username_validator],
		error_messages={
			'unique': _("A user with that username already exists."),
		},
	)
	first_name = models.CharField(_('first name'), max_length=30, default='', blank=True, null=True )
	last_name = models.CharField(_('last name'), max_length=30, default='', blank=True, null=True )
	email = models.EmailField(
		_('email address'),
		unique=True,
		help_text=_('Required. 255 characters or fewer and a valid email.'),
		error_messages={
			'unique': _("A user with that email already exists."),
		},
	)
	is_staff = models.BooleanField(
		_('staff status'),
		default=False,
		help_text=_('Designates whether the user can log into this admin site.'),
	)
	is_active = models.BooleanField(
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
	"""
	Users within the Django authentication system are represented by this
	model.

	Username, password and email are required. Other fields are optional.
	"""
	country = models.ForeignKey(Country, on_delete=models.CASCADE, default=None, blank=True, null=True )
	birthdate = models.DateField( default=None, blank=True, null=True )
	gender = models.CharField(
		max_length=1,
		choices=(('F', 'Female'),('M', 'Male'),('O', 'Other')),
		default=None,
		blank=True,
		null=True
	)

	rss_feed_title = models.CharField(max_length=100, default='', blank=True, null=True)

	description = models.TextField(default=generateDummyDesc(), blank=True, null=True)
	job = models.CharField(max_length=80, default='Chief Admission Officer at', blank=True, null=True)
	company_name = models.CharField(max_length=80, default='Holy Paradise Inc.', blank=True, null=True)
	company_website = models.URLField(max_length=120, default='http://www.feedcrunch.io/', blank=True, null=True)

	apikey = EncryptedCharField(default=uuid.uuid4, editable=False, unique=True, max_length=500)

	profile_picture = models.ImageField(upload_to=get_photo_path, default=settings.USER_PHOTO_PATH+'dummy_user.png', blank=True, null=True)

	twitter_token = EncryptedCharField(max_length=500, default='', blank=True, null=True)
	twitter_token_secret = EncryptedCharField(max_length=500, default='', blank=True, null=True)

	recommendation_engine = models.OneToOneField(Estimator, on_delete=models.CASCADE, default=None, blank=True, null=True)

	# Main Social Networks
	social_dribbble = models.URLField(max_length=60, default='', blank=True, null=True)
	social_facebook = models.URLField(max_length=60, default='', blank=True, null=True)
	social_flickr = models.URLField(max_length=60, default='', blank=True, null=True)
	social_gplus = models.URLField(max_length=60, default='', blank=True, null=True)
	social_instagram = models.URLField(max_length=60, default='', blank=True, null=True)
	social_linkedin = models.URLField(max_length=60, default='', blank=True, null=True)
	social_pinterest = models.URLField(max_length=60, default='', blank=True, null=True)
	social_stumble = models.URLField(max_length=60, default='', blank=True, null=True)
	social_twitter = models.URLField(max_length=60, default='', blank=True, null=True)
	social_vimeo = models.URLField(max_length=60, default='', blank=True, null=True)
	social_youtube = models.URLField(max_length=60, default='', blank=True, null=True)

	# Computer Science Networks
	social_docker = models.URLField(max_length=60, default='', blank=True, null=True)
	social_git = models.URLField(max_length=60, default='', blank=True, null=True)
	social_kaggle = models.URLField(max_length=60, default='', blank=True, null=True)

	# MooC Profiles
	social_coursera = models.URLField(max_length=60, default='', blank=True, null=True)

	# Research Social Networks
	social_google_scholar = models.URLField(max_length=60, default='', blank=True, null=True)
	social_orcid = models.URLField(max_length=60, default='', blank=True, null=True)
	social_researchgate = models.URLField(max_length=60, default='', blank=True, null=True)

	# Personal Webpage & Blog
	social_blog = models.URLField(max_length=60, default='', blank=True, null=True)
	social_personalwebsite = models.URLField(max_length=60, default='', blank=True, null=True)

	objects = FeedUserManager()

	class Meta(AbstractFeedUser.Meta):
			swappable = 'AUTH_USER_MODEL'

	def __unicode__(self):
		return self.username

	def get_birthdate(self):
		if self.birthdate is not None:
			return self.birthdate.strftime("%d/%m/%Y")
		else:
			return

	def is_twitter_enabled(self):
		if self.twitter_token != "" and self.twitter_token_secret != "" :
			return True
		else:
			return False

	def is_twitter_activated(self):
		if self.is_twitter_enabled() and TwitterAPI(self).verify_credentials()['status']:
			return True
		else:
			return False

	def reset_twitter_credentials(self):
		self.twitter_token = ""
		self.twitter_token_secret = ""
		self.save()

	def get_profile_picture(self):
		if settings.DEBUG:
			return self.profile_picture.url
		else:
			photo_url = "%s%s" % (settings.MEDIA_URL, self.profile_picture)
			return photo_url

	def get_post_count(self):
		return self.rel_posts.count()

	def get_current_month_post_count(self):
		d_tmp = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

		date_1st_day_month = d_tmp.replace(day=1)
		date_1st_day_month_with_tmz = timezone.make_aware(date_1st_day_month, timezone.get_current_timezone())

		return self.rel_posts.filter(when__gte=date_1st_day_month_with_tmz).count()

	def get_last_month_post_count(self):
		d_tmp = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

		time_delta = datetime.timedelta(days=1)

		date_last_day_last_month = d_tmp.replace(day=1) - time_delta
		date_1st_day_last_month = date_last_day_last_month.replace(day=1)

		date_last_day_last_month_with_tmz = timezone.make_aware(date_last_day_last_month, timezone.get_current_timezone())
		date_1st_day_last_month_with_tmz = timezone.make_aware(date_1st_day_last_month, timezone.get_current_timezone())

		return self.rel_posts.filter(when__lte=date_last_day_last_month_with_tmz, when__gte=date_1st_day_last_month_with_tmz).count()

	def get_clicks_count(self):
		return self.rel_posts.all().aggregate(models.Sum('clicks'))['clicks__sum']

	def load_opml(self, data):
		from feedcrunch.models import RSSFeed
		import untangle

		obj = untangle.parse('subscriptions.xml')

		for feed in obj.opml.body.outline:

			title = feed["title"]

			if feed["htmlUrl"] is not None:
				link = feed["htmlUrl"]
			elif feed["xmlUrl"] is not None:
				link = feed["xmlUrl"]
			else:
				continue # Go to next Feed

			if not RSSFeed.objects.filter(user=self, link=link).exists(): # Feed is Valid
				feed_tmp = RSSFeed.objects.create(user=self, title=title, link=link)

				if feed_tmp != False:
					schedule('feedcrunch.tasks.check_rss_feed', rss_id=feed_tmp.id, schedule_type=Schedule.ONCE, next_run=timezone.now() + datetime.timedelta(minutes=1))

	def refresh_user_feed(self):
		launch_time = timezone.now() + datetime.timedelta(minutes=1)

		for feed in self.rel_feeds.filter(active=True):
			schedule('feedcrunch.tasks.check_rss_feed', rss_id=feed.id, schedule_type=Schedule.ONCE, next_run=launch_time)

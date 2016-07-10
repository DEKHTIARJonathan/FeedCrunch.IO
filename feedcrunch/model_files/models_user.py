# -*- coding: utf-8 -*-
######### https://github.com/django/django/blob/master/django/contrib/auth/models.py
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, UserManager, PermissionsMixin, AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

#from django.contrib.auth.validators import *
from .validators import ASCIIUsernameValidator, UnicodeUsernameValidator
from django.utils.encoding import force_text
from django.utils import six, timezone

from django.utils.translation import ugettext_lazy as _

import os, re, uuid, datetime, unicodedata, getenv
from validate_email import validate_email
from encrypted_fields import EncryptedCharField

from twitter.tw_funcs import *

from .models_geo import *

from twython import Twython


def generateDummyDesc():
	return "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam dui nisl, aliquam nec quam nec, laoreet porta odio. Morbi ultrices sagittis ligula ut consectetur. Aenean quis facilisis augue. Vestibulum maximus aliquam augue, ut lobortis turpis euismod vel. Sed in mollis tellus, eget eleifend turpis. Vivamus aliquam ornare felis at dignissim. Integer vitae cursus eros, non dignissim dui. Suspendisse porttitor justo nec lacus dictum commodo. Sed in fringilla tortor, at pharetra tortor. Vestibulum tempor sapien id justo molestie imperdiet. Nulla efficitur mattis ante, nec iaculis lorem consequat in. Nullam sit amet diam augue. Nulla ullamcorper imperdiet turpis a maximus. Donec iaculis porttitor ultrices. Morbi lobortis dui molestie ullamcorper varius. Maecenas eu laoreet ipsum orci aliquam."

class FeedUserManager(BaseUserManager):

		use_in_migrations = True

		def _validate_username(self, username):
			if (not isinstance( username, str )) or len( username ) >= 31:
				raise ValueError("The given username is not a valid string or longer than 30 characters.")

			if not re.match("^[A-Za-z0-9]*$", username):
				raise ValueError("The given username is not a valid string, it should only contains letters (A-Z and a-z) and numbers (0-9)")

			if FeedUser.objects.filter(username = username).exists():
				raise ValueError("The given username ( "+ username +" ) is already taken")

		def _validate_email(self, email):
			if not validate_email(email):
				raise ValueError("The given email is not valid or not doesn''t exist.")

		def _validate_password(self, password):
			if re.match(r'((?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,})', password) == None:
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

			today = datetime.date.today()

			if datetime.datetime.strptime(birthdate, '%d/%m/%Y').date() > today:
				raise ValueError("The given birthdate can't be in the future. Please provide a correct date.")

		def _validate_parameters(self, username, email, password, firstname, lastname, country, gender, birthdate):

			try:
				self._validate_username(username)
				self._validate_email(email)
				self._validate_password(password)
				self._validate_firstname(firstname)
				self._validate_lastname(lastname)
				self._validate_country(country)
				self._validate_gender(gender)
				self._validate_birthdate(birthdate)

				return {'status': True}

			except Exception, e:
				return {'status': False, 'error': str(e)}

		def _normalize_username(self, username):
			return unicodedata.normalize('NFKC', force_text(username))

		def _create_user(self, username, email, password, firstname, lastname, country, gender, birthdate, **extra_fields):
				"""
				Creates and saves a User with the given username, email and password.
				"""

				is_staff = extra_fields.get('is_staff')
				is_superuser = extra_fields.get('is_superuser')

				validation = self._validate_parameters(username, email, password, firstname, lastname, country, gender, birthdate)

				if validation['status']:

					user = self.model(
						username=self._normalize_username(username),
						email=self.normalize_email(email),
						password="###", #Temporary value replaced below
						first_name=firstname,
						last_name=lastname,
						country=Country.objects.get(name=country),
						gender=gender,
						birthdate = datetime.datetime.strptime(birthdate, '%d/%m/%Y').date(),
						is_staff = is_staff,
						is_superuser = is_superuser
					)
					user.set_password(password)
					user.save(using=self._db)

					return user

				else:
					raise Exception(validation['error'])

		def create_user(self, username, email, password, firstname, lastname, country, gender, birthdate, **extra_fields):
				extra_fields.setdefault('is_staff', False)
				extra_fields.setdefault('is_superuser', False)

				try:
					return self._create_user(username, email, password, firstname, lastname, country, gender, birthdate, **extra_fields)
				except Exception, e:
					raise Exception(str(e))

		def create_superuser(self, username, email, password, firstname, lastname, country, gender, birthdate, **extra_fields):
				extra_fields.setdefault('is_staff', True)
				extra_fields.setdefault('is_superuser', True)

				if extra_fields.get('is_staff') is not True:
						raise ValueError('Superuser must have is_staff=True.')
				if extra_fields.get('is_superuser') is not True:
						raise ValueError('Superuser must have is_superuser=True.')

				try:
					return self._create_user(username, email, password, firstname, lastname, country, gender, birthdate, **extra_fields)
				except Exception, e:
					raise Exception(validation['error'])


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
	first_name = models.CharField(_('first name'), max_length=30, blank=True)
	last_name = models.CharField(_('last name'), max_length=30, blank=True)
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
	country = models.ForeignKey(Country, on_delete=models.CASCADE)
	birthdate = models.DateField()
	gender = models.CharField(
		max_length=1,
		choices=(('M', 'Male'),('F', 'Female')),
		default='M',
	)

	rss_feed_title = models.CharField(max_length=100, default='', blank=True, null=True)

	description = models.TextField(default=generateDummyDesc(), blank=True, null=True)
	job = models.CharField(max_length=80, default='Chief Admission Officer at', blank=True, null=True)
	company_name = models.CharField(max_length=80, default='Holy Paradise Inc.', blank=True, null=True)
	company_website = models.URLField(max_length=120, default='http://www.feedcrunch.io/', blank=True, null=True)

	apikey = EncryptedCharField(default=uuid.uuid4, editable=False, unique=True, max_length=500)

	profile_picture = models.ImageField(upload_to=os.path.join(settings.BASE_DIR, 'images/user_photos'), default=os.path.join(settings.BASE_DIR,'images/user_photos/dummy_user.png'), blank=True, null=True)

	twitter_token = EncryptedCharField(max_length=500, default='', blank=True, null=True)
	twitter_token_secret = EncryptedCharField(max_length=500, default='', blank=True, null=True)

	social_twitter = models.URLField(max_length=60, default='', blank=True, null=True)
	social_facebook = models.URLField(max_length=60, default='', blank=True, null=True)
	social_pinterest = models.URLField(max_length=60, default='', blank=True, null=True)
	social_gplus = models.URLField(max_length=60, default='', blank=True, null=True)
	social_dribbble = models.URLField(max_length=60, default='', blank=True, null=True)
	social_linkedin = models.URLField(max_length=60, default='', blank=True, null=True)
	social_flickr = models.URLField(max_length=60, default='', blank=True, null=True)
	social_stumble = models.URLField(max_length=60, default='', blank=True, null=True)
	social_vimeo = models.URLField(max_length=60, default='', blank=True, null=True)
	social_instagram = models.URLField(max_length=60, default='', blank=True, null=True)
	social_youtube = models.URLField(max_length=60, default='', blank=True, null=True)
	social_researchgate = models.URLField(max_length=60, default='', blank=True, null=True)
	social_personalwebsite = models.URLField(max_length=60, default='', blank=True, null=True)
	social_blog = models.URLField(max_length=60, default='', blank=True, null=True)
	social_git = models.URLField(max_length=60, default='', blank=True, null=True)

	objects = FeedUserManager()

	class Meta(AbstractFeedUser.Meta):
			swappable = 'AUTH_USER_MODEL'

	def __unicode__(self):
		return self.username

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

# -*- coding: utf-8 -*-
######### https://github.com/django/django/blob/master/django/contrib/auth/models.py
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User, UserManager, PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User
#from django.contrib.auth.validators import *
from .validators import ASCIIUsernameValidator, UnicodeUsernameValidator
from django.utils.encoding import force_text
from django.utils import six, timezone

from django.utils.translation import ugettext_lazy as _

import os, re, uuid, datetime, unicodedata, getenv
from validate_email import validate_email
from encrypted_fields import EncryptedCharField

from .models_geo import *

class FeedUserManager(BaseUserManager):
		use_in_migrations = True

		def _validate_parameters(self, username, email, password, first_name, last_name, country, sex, birth_year, birth_month, birth_day):

			today = datetime.date.today()

			if sex not in ['M', 'F']:
				raise ValueError("The given sex value is not valid : 'M' or 'F'.")

			if "CHECK_EMAIL" in os.environ and getenv.env("CHECK_EMAIL"):
				if not validate_email(email):
					raise ValueError("The given email is not valid or not doesn''t exist.")
			else:
				if not validate_email(email,verify=True):
					raise ValueError("The given email is not valid or not doesn''t exist.")

			if re.match(r'((?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,})', password) == None:
				raise ValueError("The password doesn't fit in our policies : At least 8 characters, 1 Uppercase letter 'A-Z', 1 Lowercase letter 'a-z', and 1 number '0-9'")

			if not Country.objects.filter(name = country).exists():
				raise ValueError("The given country ( "+ country +" ) doesn't exist")

			if (not isinstance( username, str )) or len( username ) >= 31:
				raise ValueError("The given username is not a valid string or longer than 30 characters.")

			if (not isinstance( first_name, str )) or len( first_name ) >= 31:
				raise ValueError("The given first_name is not a valid string or longer than 30 characters.")

			if (not isinstance( last_name, str )) or len( last_name ) >= 31:
				raise ValueError("The given last_name is not a valid string or longer than 30 characters.")

			if not isinstance( birth_year, int ):
				raise ValueError("The given birth_year value is not valid, only integer values are accepted.")

			if (not isinstance( birth_month, int )) or birth_month > 12:
				raise ValueError("The given birth_month value is not valid, only integer values are accepted and maximum value = 12.")

			if (not isinstance( birth_day, int )) or birth_day > 31:
				raise ValueError("The given birth_day value is not valid, only integer values are accepted and maximum value = 31 (depends on the month).")

			else:
				try:
					if datetime.date(birth_year, birth_month, birth_day) > today:
						raise ValueError("The given birthdate can't be in the future. Please provide a correct date.")

				except ValueError:
					raise ValueError("The given birthdate is not valid, please check the max_day for the given month")

			return True

		def _normalize_username(self, username):
			return unicodedata.normalize('NFKC', force_text(username))

		def _create_user(self, username, email, password, **extra_fields):
				"""
				Creates and saves a User with the given username, email and password.
				"""

				first_name = extra_fields.get('first_name')
				last_name = extra_fields.get('last_name')
				country = extra_fields.get('country')
				sex = extra_fields.get('sex')
				birth_year = extra_fields.get('birth_year')
				birth_month = extra_fields.get('birth_month')
				birth_day = extra_fields.get('birth_day')

				is_staff = extra_fields.get('is_staff')
				is_superuser = extra_fields.get('is_superuser')

				if self._validate_parameters(username, email, password, first_name, last_name, country, sex, birth_year, birth_month, birth_day):
					user = self.model(
						username=self._normalize_username(username),
						email=self.normalize_email(email),
						password="###", #Temporary value replaced below
						first_name=first_name,
						last_name=last_name,
						country=Country.objects.get(name=country),
						sex=sex,
						birthdate = datetime.date(birth_year, birth_month, birth_day),
						is_staff = is_staff,
						is_superuser = is_superuser
					)
					user.set_password(password)
					user.save(using=self._db)

					return user

				else:
					return False

		def create_user(self, username, email=None, password=None, **extra_fields):
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
        super(AbstractUser, self).clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
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
	apikey = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	sex = models.CharField(
		max_length=1,
		choices=(('M', 'Male'),('F', 'Female')),
		default='M',
	)

	rss_feed_title = models.CharField(max_length=100, default='')

	apikey = EncryptedCharField(default=uuid.uuid4, editable=False, unique=True, max_length=500)

	twitter_consummer_key = EncryptedCharField(max_length=500, default='')
	twitter_consummer_secret = EncryptedCharField(max_length=500, default='')
	twitter_token = EncryptedCharField(max_length=500, default='')
	twitter_token_secret = EncryptedCharField(max_length=500, default='')

	objects = FeedUserManager()

	class Meta(AbstractFeedUser.Meta):
			swappable = 'AUTH_USER_MODEL'

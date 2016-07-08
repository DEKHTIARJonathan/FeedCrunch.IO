# -*- coding: utf-8 -*-
from django.core import management

import sys, datetime, factory, time

from .models import Post, FeedUser

class UserFactory(factory.DjangoModelFactory):
	class Meta:
		model = FeedUser

	username="testuser1"
	email="marco.flint31@gmail.com"
	password="DummyPassword123"
	firstname="test"
	lastname="USER1"
	country="France"
	gender="M"
	birthdate="01/01/2000"

	@classmethod
	def _create(cls, model_class, *args, **kwargs):
		global init_test_db

		"""Override the default ``_create`` with our custom call."""
		manager = cls._get_manager(model_class)

		# The default would use ``manager.create(*args, **kwargs)``
		return manager.create_user(*args, **kwargs)

class PostFactory(factory.DjangoModelFactory):
	class Meta:
		model = Post

	title = "Post's Title"
	link = "http://www.google.com/"
	clicks = 100
	activeLink = True
	user = factory.SubFactory(UserFactory)

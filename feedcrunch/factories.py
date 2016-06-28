from django.core import management

import sys, datetime, factory, time

from .models import Post, FeedUser

class UserFactory(factory.DjangoModelFactory):
	class Meta:
		model = FeedUser

	username="test_user1"
	email="contact@dataradar.io"
	password="DummyPassword123"
	first_name="test"
	last_name="USER1"
	country="France"
	sex="M"
	birth_year=2000
	birth_month=1
	birth_day=1

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

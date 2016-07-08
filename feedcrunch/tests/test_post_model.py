# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from feedcrunch.models import Post, FeedUser
from feedcrunch.factories import *
from application.settings import *

import factory, datetime

class PostTest(TestCase):

	def setUp(self):
		self.dummy_user = UserFactory()
		self.dummy_user.save()
		self.dummy_post = PostFactory()
		self.dummy_post.save()

	@classmethod
	def setUpTestData(self):
		# Set up data for the whole TestCase
		from django.core.management import call_command
		call_command(
			'loaddata',
			'feedcrunch_dump.json'
		)

	def tearDown(self):
		self.dummy_post.delete()
		self.dummy_user.delete()

	def test_get_domain(self):
		domain = self.dummy_post.get_domain()
		self.assertIsInstance(domain, str)
		self.assertEqual(domain, "www.google.com")

	def test_get_domain_short(self):
		post = PostFactory(link="http://www.google.com")
		domain = post.get_domain()
		self.assertIsInstance(domain, str)
		self.assertEqual(domain, "www.google.com")

	def test_get_domain_error(self):
		post = PostFactory(link="blabla")
		domain = post.get_domain()
		self.assertIsInstance(domain, str)
		self.assertEqual(domain, "error")

	def test_get_date(self):
		date = self.dummy_post.get_date()
		self.assertIsInstance(date, str)
		self.assertTrue(self.validate_date(date))


	def test_validate_date_ok(self):
		date = "2016/06/11 22:36"
		self.assertTrue(self.validate_date(date))

	def test_validate_date_ko(self):
		date = "2016/21/01 22:36"
		with self.assertRaises(ValueError):
			self.validate_date(date)

	def validate_date(self, date_text):
		try:
			datetime.datetime.strptime(date_text, '%Y/%m/%d %H:%M')
			return True
		except ValueError:
			raise ValueError("Incorrect data format, should be %Y/%m/%d %H:%M")

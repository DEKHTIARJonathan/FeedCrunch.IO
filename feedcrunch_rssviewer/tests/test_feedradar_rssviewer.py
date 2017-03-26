#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from feedcrunch.models import Post
from application.settings import *

from feedcrunch.factories import *

import factory
from feedparser import parse

from rss_generator import generateRSS
# Create your tests here.

class feedcrunch_rssviewer_TestCase(TestCase):
    def setUp(self):
        self.client = Client()
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

    def test_index_page(self):
        url = reverse('index', kwargs={'feedname':"testuser1"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rssviewer.html')
        self.assertContains(response, 'RSS Feed Explorer')

    def test_rss_feed(self):
        url = reverse('rss_feed', kwargs={'feedname':"testuser1"})
        response = self.client.get(url)
        myfeed = parse(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(myfeed.entries), 1)
        self.assertContains(response, "Post's Title")

    def test_atom_feed(self):
        url = reverse('atom_feed', kwargs={'feedname':"testuser1"})
        response = self.client.get(url)
        myfeed = parse(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(myfeed.entries), 1)
        self.assertContains(response, "Post's Title")

    def test_generateRSS(self):
        with self.assertRaises(ValueError):
            tmp = generateRSS()

    def test_RSS_with_No_Data(self):
        self.dummy_post.delete()

        url = reverse('rss_feed', kwargs={'feedname':"testuser1"})
        response = self.client.get(url)
        myfeed = parse(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(myfeed.entries), 0)
        self.assertContains(response, "No Entries in this feed yet")

        url = reverse('atom_feed', kwargs={'feedname':"testuser1"})
        response = self.client.get(url)
        myfeed = parse(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(myfeed.entries), 0)
        self.assertContains(response, "No Entries in this feed yet")

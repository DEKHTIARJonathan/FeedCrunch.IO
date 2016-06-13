from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from dataradar.models import Article

from dataradar_webviewer.functions import *

import factory
from feedparser import parse
# Create your tests here.

class ArticleFactory(factory.Factory):
    class Meta:
        model = Article

    title = "Article's Title"
    link = "http://www.google.com/"
    clicks = 100
    activeLink = True

class dataradar_webviewer_TestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.dummy_article = ArticleFactory()
        self.dummy_article.save()

    def tearDown(self):
        self.dummy_article.delete()

    def test_index_page(self):
         url = reverse('index')
         response = self.client.get(url)
         self.assertEqual(response.status_code, 200)
         self.assertTemplateUsed(response, 'index.html')
         self.assertContains(response, 'DataRadar.IO - Do you have enough data about your #data?')

    def test_rss_feed(self):
         url = reverse('rss_feed')
         response = self.client.get(url)
         myfeed = parse(response.content)
         self.assertEqual(response.status_code, 200)
         self.assertEqual(len(myfeed.entries), 1)
         self.assertContains(response, "Article's Title")

    def test_atom_feed(self):
         url = reverse('atom_feed')
         response = self.client.get(url)
         myfeed = parse(response.content)
         self.assertEqual(response.status_code, 200)
         self.assertEqual(len(myfeed.entries), 1)
         self.assertContains(response, "Article's Title")

    def test_generateRSS(self):
        with self.assertRaises(ValueError):
            tmp = generateRSS()

    def test_RSS_with_No_Data(self):
        self.dummy_article.delete()

        url = reverse('rss_feed')
        response = self.client.get(url)
        myfeed = parse(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(myfeed.entries), 0)
        self.assertContains(response, "No Entries in this feed yet")

        url = reverse('atom_feed')
        response = self.client.get(url)
        myfeed = parse(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(myfeed.entries), 0)
        self.assertContains(response, "No Entries in this feed yet")

        self.dummy_article = ArticleFactory()
        self.dummy_article.save()

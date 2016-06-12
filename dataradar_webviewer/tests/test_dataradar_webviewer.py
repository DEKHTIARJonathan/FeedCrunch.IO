from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from dataradar.models import Article

import factory
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

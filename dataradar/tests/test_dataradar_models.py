from django.test import TestCase
from dataradar.models import Article

import factory, datetime
# Create your tests here.

class ArticleFactory(factory.Factory):
    class Meta:
        model = Article

    title = "Article's Title"
    link = "http://www.google.com/foo/bar.html"
    clicks = 100
    activeLink = True


class ArticleTest(TestCase):

    def setUp(self):
        self.dummy_article = ArticleFactory()
        self.dummy_article.save()

    def tearDown(self):
        self.dummy_article.delete()

    def test_get_domain(self):
        domain = self.dummy_article.get_domain()
        self.assertIsInstance(domain, str)
        self.assertEqual(domain, "www.google.com")

    def test_get_domain_short(self):
        article = ArticleFactory(link="http://www.google.com")
        domain = article.get_domain()
        self.assertIsInstance(domain, str)
        self.assertEqual(domain, "www.google.com")

    def test_get_domain_error(self):
        article = ArticleFactory(link="blabla")
        domain = article.get_domain()
        self.assertIsInstance(domain, str)
        self.assertEqual(domain, "error")

    def test_get_date(self):
        date = self.dummy_article.get_date()
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

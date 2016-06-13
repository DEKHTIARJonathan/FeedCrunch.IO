from django.shortcuts import render
from django.http import HttpResponse

from dataradar.models import Article

from feedgen.feed import FeedGenerator
from .functions import *

# Create your views here.

def index(request):
    articles = Article.objects.all()
    return render(request, 'index.html', {'articles': articles})



def rss_feed(request):
    if Article.objects.count() > 0:
        fg = generateRSS("rss")
        return HttpResponse(fg.rss_str(pretty=True, encoding='UTF-8'), content_type='application/xml')
    else:
        return HttpResponse("No Entries in this feed yet")

def atom_feed(request):
    if Article.objects.count() > 0:
        fg = generateRSS("atom")
        return HttpResponse(fg.atom_str(pretty=True, encoding='UTF-8'), content_type='application/xml')
    else:
        return HttpResponse("No Entries in this feed yet")

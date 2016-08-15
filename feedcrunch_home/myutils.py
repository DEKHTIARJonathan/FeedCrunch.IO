# -*- coding: utf-8 -*-
from django.shortcuts import render
from feedcrunch.models import FeedUser

def myrender(request, template, dictionary):
	dictionary.update({'template_name': template})
	dictionary.update({'user_count': FeedUser.objects.count()})
	
	return render(request, template, dictionary)

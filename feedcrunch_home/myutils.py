# -*- coding: utf-8 -*-
from django.shortcuts import render

def myrender(request, template, dictionary):
	dictionary.update({'template_name': template})
	return render(request, template, dictionary)

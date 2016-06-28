from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response

def index(request):
    response = render_to_response('index_home.html')
    response.status_code = 200
    return response

def handler404(request):
    response = render_to_response('404.html')
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('500.html')
    response.status_code = 500
    return response

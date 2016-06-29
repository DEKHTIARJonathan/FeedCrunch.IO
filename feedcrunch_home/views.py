from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import authenticate, login, logout

def index(request):
    response = render_to_response('index_home.html')
    response.status_code = 200
    return response

def faq(request):
    response = render_to_response('faq.html')
    response.status_code = 200
    return response

def contact(request):
    response = render_to_response('contact.html')
    response.status_code = 200
    return response

def about(request):
    response = render_to_response('about.html')
    response.status_code = 200
    return response

def loginView(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/@'+request.user.username+'/admin')

            else:
                return HttpResponse("Your account is inactive.")
        else:
            return redirect('/login/')
    else:
        return render(request, 'login.html')

#@login_required(login_url='/login/')
def test(request):
    return HttpResponse("Welcome.")

def handler404(request):
    response = render_to_response('404.html')
    response.status_code = 404
    return response

def handler500(request):
    response = render_to_response('500.html')
    response.status_code = 500
    return response

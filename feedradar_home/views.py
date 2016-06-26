from django.http import HttpResponse
from django.template import RequestContext, loader

def index(request):
    template = loader.get_template('index_home.html')
    context = RequestContext(request, {} )
    return HttpResponse(template.render(context))
    #return render_to_response("index.html", {},context_instance=RequestContext(request))

def handler404(request):
    response = render_to_response('404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('500.html', {}, context_instance=RequestContext(request))
    response.status_code = 500
    return response

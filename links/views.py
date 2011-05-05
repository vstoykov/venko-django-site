from django.template import RequestContext
from django.shortcuts import render_to_response

from links.models import Link

def links(request):
    links = Link.objects.order_by('category')
    return render_to_response('links.html', locals(), RequestContext(request))
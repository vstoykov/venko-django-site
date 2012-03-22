from django.template import RequestContext
from django.shortcuts import render_to_response

from blog.models import Entry


def home(request):
    latest = Entry.objects.order_by('-created')[:4]
    show_more_link = len(latest) == 4
    latest = latest[:3]
    return render_to_response('home.html', locals(), RequestContext(request))

def gallery(request):
    return render_to_response('gallery.html')


#def about(request):
#    return render_to_response('about_me.html')

#def links(request):
#    return render_to_response('links.html')

#def contact(request):
#    return render_to_response('contact_me.html')

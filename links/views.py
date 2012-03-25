from django.views.generic.simple import direct_to_template

from links.models import Link

def links(request, template="links.html"):
    return direct_to_template(request, template, {
        'links': Link.objects.order_by('category')
        })

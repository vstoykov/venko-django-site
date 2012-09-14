from django.shortcuts import render

from links.models import Link


def links(request, template="links.html"):
    return render(request, template, {
        'links': Link.objects.order_by('category')
        })

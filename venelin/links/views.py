from django.shortcuts import render

from .models import Link


def links(request, template="links.html"):
    return render(request, template, {
        'links': Link.objects.select_related('category').order_by('category')
    })

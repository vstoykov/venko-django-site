from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_safe

from .ajax import json_view
from .models import Gallery


@require_safe
def galleries(request):
    galleries = Gallery.objects.active()
    return render(request, 'galleries.html', {'galleries': galleries})


@require_safe
def gallery(request, slug):
    gallery = get_object_or_404(Gallery.objects.active(), slug=slug)
    return render(request, 'gallery.html', {'gallery': gallery})


#############
# API Views #
#############


@json_view
@require_safe
def galleries_json(request):
    galleries = Gallery.objects.active()
    response = {
        'data': [{
            'title': gallery.title,
            'slug': gallery.slug,
            'cover': gallery.get_thumbnail_url(),
        } for gallery in galleries]
    }
    return response


@json_view
@require_safe
def gallery_json(request, slug):
    gallery = get_object_or_404(Gallery.objects.active(), slug=slug)
    response = {
        'data': {
            'slug': gallery.slug,
            'title': gallery.title,
            'pictures': [{
                'title': picture.title,
                'image': picture.image.url,
                'thumb': picture.thumb.url,
            } for picture in gallery.pictures.all()]
        }
    }
    return response

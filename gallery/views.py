from django.shortcuts import render, get_object_or_404

from gallery.models import Gallery


def galleries(request):
    galleries = Gallery.objects.exclude(pictures=None)
    return render(request, 'galleries.html', {'galleries': galleries})

def gallery(request, slug):
    gallery = get_object_or_404(Gallery, slug=slug)
    return render(request, 'gallery.html', {'gallery': gallery})
